"""
Single-file FastAPI application
- Run: python fastapi_single_file_app.py
- Features:
  - Pydantic models for request/response
  - In-memory CRUD for "items"
  - File upload endpoint
  - WebSocket echo endpoint
  - Background task example
  - CORS enabled
  - Simple dependency and middleware example

This is intentionally self-contained for easy testing and quick portfolio/demo usage.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from uuid import uuid4
from datetime import datetime
import uvicorn
import asyncio

app = FastAPI(title="FastAPI Single-file App", version="1.0")

# --- CORS (useful for frontend demos) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # be stricter in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simple request logging middleware (example) ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response

# --- Models ---
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)

class Item(ItemCreate):
    id: str
    created_at: datetime

class HealthResponse(BaseModel):
    status: str
    time: datetime

# --- In-memory store ---
_items: Dict[str, Item] = {}

# --- Dependency example ---
def get_fake_db():
    # placeholder for real DB session dependency
    return _items

# --- CRUD endpoints ---
@app.get("/", tags=["root"])
async def root():
    return {"message": "FastAPI single-file app running", "version": app.version}

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    return HealthResponse(status="ok", time=datetime.utcnow())

@app.post("/items", response_model=Item, status_code=201, tags=["items"])
async def create_item(item: ItemCreate, db: Dict[str, Item] = Depends(get_fake_db), background_tasks: BackgroundTasks = None):
    item_id = str(uuid4())
    new_item = Item(id=item_id, created_at=datetime.utcnow(), **item.dict())
    db[item_id] = new_item

    # background task example: pretend to index into a search service
    if background_tasks is not None:
        background_tasks.add_task(_background_index_item, new_item)
    return new_item

async def _background_index_item(item: Item):
    # simulate network call / indexing
    await asyncio.sleep(0.3)
    print(f"[background] indexed item {item.id}")

@app.get("/items", response_model=List[Item], tags=["items"])
async def list_items(skip: int = 0, limit: int = 50, db: Dict[str, Item] = Depends(get_fake_db)):
    items = list(db.values())[skip: skip + limit]
    return items

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def get_item(item_id: str, db: Dict[str, Item] = Depends(get_fake_db)):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: str, payload: ItemCreate, db: Dict[str, Item] = Depends(get_fake_db)):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = Item(id=item_id, created_at=item.created_at, **payload.dict())
    db[item_id] = updated
    return updated

@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def delete_item(item_id: str, db: Dict[str, Item] = Depends(get_fake_db)):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return None

# --- File upload example ---
@app.post("/upload", tags=["files"])
async def upload_file(file: UploadFile = File(...)):
    # caution: this keeps file in memory for small files only
    contents = await file.read()
    size = len(contents)
    # in a real app, write to disk or object storage
    return {"filename": file.filename, "content_type": file.content_type, "size": size}

# --- WebSocket simple echo ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"echo: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")

# --- Simple metrics endpoint (minimal) ---
@app.get("/metrics", tags=["metrics"])
async def metrics():
    return {"items_count": len(_items)}

# --- Run with: python fastapi_single_file_app.py ---
if __name__ == "__main__":
    # Use uvicorn programmatically so it's single-file runnable
    uvicorn.run("fastapi_single_file_app:app", host="0.0.0.0", port=8000, reload=False)
