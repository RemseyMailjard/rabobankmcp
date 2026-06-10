import uvicorn


def main() -> None:
    uvicorn.run("app.internal_api:app", host="127.0.0.1", port=8000, reload=True)
