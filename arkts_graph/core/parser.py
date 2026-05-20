import re
import hashlib
from pathlib import Path
from .models import (
    ParsedFile,
    ClassEntity,
    MethodEntity,
    CallRelationship,
    ComponentRelationship,
)


class ArkTSParser:
    def __init__(self):
        self.class_pattern = re.compile(r"class\s+(\w+)")
        self.method_pattern = re.compile(r"(\w+)\s*\([^)]*\)\s*\{")
        self.call_pattern = re.compile(r"(\w+)\s*\(")
        self.component_pattern = re.compile(r"<(\w+)")

    def parse(self, file_path: Path) -> ParsedFile:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        file_hash = self._compute_hash(content)
        classes = self._extract_classes(content)
        methods = self._extract_methods(content, classes)
        calls = self._extract_calls(content, methods)
        components = self._extract_components(content, classes)
        return ParsedFile(
            path=file_path,
            file_hash=file_hash,
            classes=classes,
            methods=methods,
            calls=calls,
            components=components,
        )

    @staticmethod
    def _compute_hash(content: str) -> bytes:
        return hashlib.md5(content.encode("utf-8")).digest()

    def _extract_classes(self, content: str) -> list[ClassEntity]:
        classes = []
        for match in self.class_pattern.finditer(content):
            class_name = match.group(1)
            classes.append(ClassEntity(name=class_name))
        return classes

    def _extract_methods(self, content: str, classes: list[ClassEntity]) -> list[MethodEntity]:
        methods = []
        class_names = [c.name for c in classes]
        if class_names:
            current_class = class_names[0]
            for match in self.method_pattern.finditer(content):
                method_name = match.group(1)
                if method_name in class_names:
                    current_class = method_name
                methods.append(MethodEntity(name=f"{current_class}::{method_name}"))
        else:
            for match in self.method_pattern.finditer(content):
                method_name = match.group(1)
                methods.append(MethodEntity(name=f"Global::{method_name}"))
        return methods

    def _extract_calls(self, content: str, methods: list[MethodEntity]) -> list[CallRelationship]:
        calls = []
        method_names = [m.name for m in methods]
        method_map = {m.name: i for i, m in enumerate(methods)}
        current_method_idx = 0
        for match in self.call_pattern.finditer(content):
            called = match.group(1)
            for i, method in enumerate(methods):
                if called in method.name or method.name.endswith(called):
                    current_method_idx = i
                    break
            full_name = f"Global::{called}"
            if full_name in method_map:
                caller_id = current_method_idx
                callee_id = method_map[full_name]
                if caller_id != callee_id:
                    calls.append(CallRelationship(caller_id=caller_id, callee_id=callee_id))
        return calls

    def _extract_components(self, content: str, classes: list[ClassEntity]) -> list[ComponentRelationship]:
        components = []
        class_map = {c.name: i for i, c in enumerate(classes)}
        for match in self.component_pattern.finditer(content):
            comp_name = match.group(1)
            if comp_name in class_map and class_map[comp_name] != 0:
                components.append(
                    ComponentRelationship(
                        parent_id=0,
                        child_id=class_map[comp_name],
                    )
                )
        return components
