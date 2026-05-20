import time
import threading
from pathlib import Path
from typing import Optional, Callable
from .models import FileChangeEvent, ChangeType, ParsedFile
from .database import Database
from .parser import ArkTSParser
from .watcher import FileWatcher
from .queue import ChangeQueue


class UpdateEngine:
    def __init__(
        self,
        project_path: Path,
        db: Database,
        debounce_window: float = 1.0,
        on_update: Optional[Callable[[str, float], None]] = None,
    ):
        self.project_path = project_path
        self.db = db
        self.parser = ArkTSParser()
        self.queue = ChangeQueue(debounce_window=debounce_window)
        self.watcher = FileWatcher(project_path)
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        self._on_update = on_update

    def full_sync(self) -> tuple[int, float]:
        start_time = time.time()
        count = 0
        for ext in [".ets", ".ts", ".tsx"]:
            for file_path in self.project_path.rglob(f"*{ext}"):
                if any(excl in file_path.parts for excl in [".git", "node_modules", "build", "dist"]):
                    continue
                self._update_single_file(file_path, ChangeType.CREATED)
                count += 1
        elapsed = time.time() - start_time
        return count, elapsed

    def _update_single_file(self, file_path: Path, change_type: ChangeType):
        start = time.time()
        if change_type in (ChangeType.MODIFIED, ChangeType.DELETED):
            self.db.delete_file_data(file_path)
        if change_type in (ChangeType.CREATED, ChangeType.MODIFIED):
            if file_path.exists():
                parsed = self.parser.parse(file_path)
                self.db.insert_parsed_file(parsed)
        elapsed = time.time() - start
        if self._on_update:
            self._on_update(str(file_path), elapsed)
        return elapsed

    def _worker_loop(self):
        while self._running:
            try:
                batch = self.queue.get_batch(timeout=0.5)
                for event in batch:
                    self._update_single_file(event.path, event.change_type)
            except Exception as e:
                print(f"Error processing batch: {e}")

    def start(self):
        self._running = True
        self.watcher.start(self.queue.add)
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def stop(self):
        self._running = False
        self.watcher.stop()
        if self._worker_thread:
            self._worker_thread.join(timeout=2.0)

    def is_running(self) -> bool:
        return self._running
