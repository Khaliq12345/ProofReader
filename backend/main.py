import asyncio
import os
import sys
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import socketio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Pour compatibilité Windows (Python ≥3.8)
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configuration
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), 'outputs')
PORT = 8000

# Ensure outputs directory exists
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Setup FastAPI + Socket.io
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = FastAPI()
asgi_app = socketio.ASGIApp(sio, app)

# Serve file downloads
@app.get('/files/{filename}')
async def download_file(filename: str):
    file_path = os.path.join(OUTPUTS_DIR, filename)
    if os.path.isfile(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail='File not found')

# Helper: get current list of files
def list_current_files() -> List[str]:
    return [
        f for f in os.listdir(OUTPUTS_DIR)
        if os.path.isfile(os.path.join(OUTPUTS_DIR, f))
    ]

# Emit the initial file list to a specific client
async def emit_initial_files(sid):
    files = list_current_files()
    await sio.emit('initial-files', files, to=sid)
    print(f"Sent initial files to {sid}: {files}")

# Watchdog handler
class OutputsHandler(FileSystemEventHandler):
    def __init__(self, loop):
        super().__init__()
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            asyncio.run_coroutine_threadsafe(
                sio.emit('file-added', filename), self.loop
            )
            print(f"File added: {filename}")

    def on_deleted(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            asyncio.run_coroutine_threadsafe(
                sio.emit('file-removed', filename), self.loop
            )
            print(f"File removed: {filename}")

# Get current event loop
loop = asyncio.get_event_loop()

# Setup observer
event_handler = OutputsHandler(loop)
observer = Observer()
observer.schedule(event_handler, OUTPUTS_DIR, recursive=False)
observer.start()
print(f"Started watching directory: {OUTPUTS_DIR}")

# Socket.io events
@sio.event
async def connect(sid, environ):
    print(f'Client connected: {sid}')
    await emit_initial_files(sid)

@sio.event
def disconnect(sid):
    print(f'Client disconnected: {sid}')

