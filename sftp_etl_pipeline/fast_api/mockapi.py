# mock_api.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/dummy-query")
async def handle_query(req: QueryRequest):
    # Dummy data you might get from a database
    fake_data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    return JSONResponse(content={"results": fake_data})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
