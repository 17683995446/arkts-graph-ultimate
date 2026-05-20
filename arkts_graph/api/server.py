from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from .routes import create_api_router
from ..core import Database, UpdateEngine


class APIServer:
    def __init__(self, project_path: Path, db_path: Path, host: str = "0.0.0.0", port: int = 8000):
        self.project_path = project_path
        self.db_path = db_path
        self.host = host
        self.port = port
        self.db: Optional[Database] = None
        self.engine: Optional[UpdateEngine] = None
        self.app: Optional[FastAPI] = None

    def _create_app(self) -> FastAPI:
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            self.db = Database(self.db_path)
            self.engine = UpdateEngine(
                self.project_path,
                self.db,
                on_update=self._on_update,
            )
            print("Performing initial full sync...")
            count, elapsed = self.engine.full_sync()
            print(f"Full sync complete: {count} files in {elapsed:.2f}s")
            self.engine.start()
            yield
            self.engine.stop()
            self.db.close()

        app = FastAPI(title="ArkTS Knowledge Graph", lifespan=lifespan)
        web_dir = Path(__file__).parent.parent / "web"
        app.mount("/static", StaticFiles(directory=str(web_dir / "static")), name="static")
        self.templates = Jinja2Templates(directory=str(web_dir / "templates"))

        @app.get("/", response_class=HTMLResponse)
        async def index(request: Request):
            stats = self.db.get_stats()
            return self.templates.TemplateResponse("index.html", {"request": request, "stats": stats})

        api_router = create_api_router(self.db)
        app.include_router(api_router, prefix="/api")
        return app

    def _on_update(self, path: str, elapsed: float):
        print(f"Updated {path} in {elapsed:.3f}s")

    def run(self):
        import uvicorn

        self.app = self._create_app()
        uvicorn.run(self.app, host=self.host, port=self.port)
