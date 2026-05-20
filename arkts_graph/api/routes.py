from fastapi import APIRouter
from ..core import Database


def create_api_router(db: Database) -> APIRouter:
    router = APIRouter()

    @router.get("/stats")
    async def get_stats():
        return db.get_stats()

    @router.get("/classes")
    async def get_classes():
        classes = db.get_classes()
        return [{"id": c.id, "name": c.name, "file_id": c.file_id} for c in classes]

    @router.get("/methods")
    async def get_methods():
        methods = db.get_methods()
        return [{"id": m.id, "name": m.name, "class_id": m.class_id} for m in methods]

    @router.get("/graph/calls")
    async def get_call_graph():
        calls = db.get_call_graph()
        return [{"source": c[0], "target": c[1]} for c in calls]

    @router.get("/graph/components")
    async def get_component_graph():
        components = db.get_component_graph()
        return [{"source": c[0], "target": c[1]} for c in components]

    @router.get("/files")
    async def get_files():
        files = db.get_all_files()
        return [{"id": f.id, "path": str(f.path), "modified": f.modified} for f in files]

    return router
