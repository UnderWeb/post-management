from fastapi import FastAPI

app = FastAPI(
    title="BTG Posts Management API",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
