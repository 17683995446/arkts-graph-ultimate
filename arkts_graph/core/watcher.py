import time
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from .models import FileChangeEvent, ChangeType


class _FileHandler(FileSystemEventHandler):
    def __init__(
        self,
        callback: Callable[[FileChangeEvent], None],
        extensions: tuple,
        exclude_dirs: tuple,
    ):
        super().__init__()
        self.callback = callback
        self.extensions = extensions
        self.exclude_dirs = exclude_dirs

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory:
            return
        path = Path(event.src_path)
        for excl in self.exclude_dirs:
            if excl in path.parts:
                return
        if path.suffix not in self.extensions:
            return
        if event.event_type == "created":
            change_type = ChangeType.CREATED
        elif event.event_type == "modified":
            change_type = ChangeType.MODIFIED
        elif event.event_type == "deleted":
            change_type = ChangeType.DELETED
        else:
            return
        self.callback(
            FileChangeEvent(
                path=path,
                change_type=change_type,
                timestamp=time.time(),
            )
        )


class FileWatcher:
    def __init__(
        self,
        project_path: Path,
        extensions: tuple = (".ets", ".ts", ".tsx"),
        exclude_dirs: tuple = (".git", "node_modules"),
    ):
        self.project_path = project_path
        self.extensions = extensions
        self.exclude_dirs = exclude_dirs
        self.observer: Optional[Observer] = None
        self._running = False

    def start(self, callback: Callable[[FileChangeEvent], None]):
        self.observer = Observer()
        handler = _FileHandler(callback, self.extensions, self.exclude_dirs)
        self.observer.schedule(handler, str(self.project_path), recursive=True)
        self.observer.start()
        self._running = True

    def stop(self):
        if self.observer and self._running:
            self.observer.stop()
            self.observer.join()
            self._running = False

    def is_running(self) -> bool:
        return self._running
