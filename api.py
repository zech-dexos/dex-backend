from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dex_runtime import dex_runtime

app = FastAPI(title="ReasonFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    input: str

@app.post("/analyze")
def analyze(req: Request):
    return dex_runtime(req.input)

@app.get("/health")
def health():
    return {"status": "live"}

@app.get("/")
def index():
    return FileResponse("index.html")

app.mount("/static", StaticFiles(directory="."), name="static")
