import time
import pytest
from pathlib import Path
from arkts_graph.core.queue import ChangeQueue
from arkts_graph.core.models import FileChangeEvent, ChangeType


def test_queue_initialization():
    queue = ChangeQueue()
    assert queue.is_empty() is True


def test_queue_add_event():
    queue = ChangeQueue()
    event = FileChangeEvent(
        path=Path("test.ets"),
        change_type=ChangeType.MODIFIED,
        timestamp=time.time(),
    )
    queue.add(event)
    assert queue.is_empty() is False
    assert queue.size() == 1


def test_queue_get_batch(temp_dir):
    queue = ChangeQueue(debounce_window=0.1)
    event = FileChangeEvent(
        path=Path("test.ets"),
        change_type=ChangeType.MODIFIED,
        timestamp=time.time(),
    )
    queue.add(event)
    batch = queue.get_batch(timeout=1.0)
    assert len(batch) == 1
    assert batch[0].path == Path("test.ets")
    assert queue.is_empty() is True


def test_queue_duplicate_events():
    queue = ChangeQueue(debounce_window=0.1)
    path = Path("test.ets")
    event1 = FileChangeEvent(
        path=path,
        change_type=ChangeType.MODIFIED,
        timestamp=time.time(),
    )
    event2 = FileChangeEvent(
        path=path,
        change_type=ChangeType.MODIFIED,
        timestamp=time.time() + 0.01,
    )
    queue.add(event1)
    queue.add(event2)
    assert queue.size() == 1
