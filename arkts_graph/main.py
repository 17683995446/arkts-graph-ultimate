#!/usr/bin/env python3
import argparse
from pathlib import Path
from .api import APIServer


def main():
    parser = argparse.ArgumentParser(description="ArkTS Knowledge Graph - Real-time Code Analysis")
    parser.add_argument(
        "--project",
        "-p",
        type=Path,
        default=Path("."),
        help="Path to the project directory",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("knowledge_graph.db"),
        help="Path to the database file",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    args = parser.parse_args()
    server = APIServer(
        project_path=args.project.resolve(),
        db_path=args.db.resolve(),
        host=args.host,
        port=args.port,
    )
    server.run()


if __name__ == "__main__":
    main()
