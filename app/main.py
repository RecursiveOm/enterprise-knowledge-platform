from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Intelligence Platform"
)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
