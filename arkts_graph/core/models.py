from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


class ChangeType(Enum):
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"


@dataclass
class FileChangeEvent:
    path: Path
    change_type: ChangeType
    timestamp: float


@dataclass
class FileEntity:
    id: Optional[int] = None
    path: Optional[Path] = None
    hash: Optional[bytes] = None
    modified: Optional[int] = None


@dataclass
class ClassEntity:
    name: str
    id: Optional[int] = None
    file_id: Optional[int] = None
    flags: int = 0


@dataclass
class MethodEntity:
    name: str
    id: Optional[int] = None
    class_id: Optional[int] = None


@dataclass
class CallRelationship:
    caller_id: int
    callee_id: int


@dataclass
class ComponentRelationship:
    parent_id: int
    child_id: int


@dataclass
class ParsedFile:
    path: Path
    file_hash: bytes
    classes: list[ClassEntity] = field(default_factory=list)
    methods: list[MethodEntity] = field(default_factory=list)
    calls: list[CallRelationship] = field(default_factory=list)
    components: list[ComponentRelationship] = field(default_factory=list)
