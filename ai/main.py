import sys
import queue
import threading
import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from ai.agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RerouteRequest(BaseModel):
    ship_id: str

@contextlib.contextmanager
def redirect_stdout_to_queue(q):
    old_stdout = sys.stdout
    class WriteQueue:
        def write(self, data):
            if data:
                q.put(data)
            return len(data)
        def flush(self):
            pass
    sys.stdout = WriteQueue()
    try:
        yield
    finally:
        sys.stdout = old_stdout

@app.post("/api/reroute")
def reroute_ship(req: RerouteRequest):
    q = queue.Queue()

    def run_in_thread():
        with redirect_stdout_to_queue(q):
            try:
                result = run_agent(req.ship_id)
                q.put(f"\n__RESULT__\n{result}")
            except Exception as e:
                q.put(f"\n__ERROR__\n{str(e)}")
            finally:
                q.put(None)

    threading.Thread(target=run_in_thread).start()

    def event_generator():
        while True:
            chunk = q.get()
            if chunk is None:
                break
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")
