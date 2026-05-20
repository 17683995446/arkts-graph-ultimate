from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    project_path: Path
    db_path: Path
    debounce_window: float = 1.0
    max_queue_size: int = 100
    watch_extensions: tuple = (".ets", ".ts", ".tsx")
    exclude_dirs: tuple = (".git", "node_modules", "build", "dist")
