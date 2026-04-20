from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    input: str

@app.post("/dex")
def run(req: Request):
    return {
        "output": f"Dex received: {req.input}",
        "selected_path": "decompose"
    }
