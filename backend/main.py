from fastapi import FastAPI

from server import mcp_app

app = FastAPI(lifespan=mcp_app.lifespan)

app.mount("/mcp", mcp_app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
