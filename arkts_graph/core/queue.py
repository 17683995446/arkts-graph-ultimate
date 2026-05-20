import time
import threading
from collections import defaultdict
from pathlib import Path
from typing import Optional
from .models import FileChangeEvent, ChangeType


class ChangeQueue:
    def __init__(self, debounce_window: float = 1.0, max_size: int = 100):
        self.debounce_window = debounce_window
        self.max_size = max_size
        self._queue: dict[Path, FileChangeEvent] = {}
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)

    def add(self, event: FileChangeEvent):
        with self._lock:
            self._queue[event.path] = event
            if len(self._queue) > self.max_size:
                paths = sorted(self._queue.keys(), key=lambda p: self._queue[p].timestamp)
                for path in paths[: len(self._queue) - self.max_size]:
                    del self._queue[path]
            self._not_empty.notify()

    def get_batch(self, timeout: Optional[float] = None) -> list[FileChangeEvent]:
        with self._lock:
            if not self._queue:
                if timeout is None:
                    self._not_empty.wait()
                else:
                    self._not_empty.wait(timeout=timeout)
            time.sleep(self.debounce_window)
            batch = list(self._queue.values())
            self._queue.clear()
            return batch

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._queue) == 0

    def size(self) -> int:
        with self._lock:
            return len(self._queue)
