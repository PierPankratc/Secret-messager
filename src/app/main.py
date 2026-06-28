from fastapi import FastAPI
import uvicorn

from src.app.crypto import fernet
from src.db.create_db import Base, engine
from src.routers.links import router as link_router
from src.routers.messages import router as message_router
from src.routers.users import router as user_router

app = FastAPI(title="secrets-messager")
app.include_router(user_router)
app.include_router(message_router)
app.include_router(link_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}


Base.metadata.create_all(bind=engine)


def main() -> None:
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
