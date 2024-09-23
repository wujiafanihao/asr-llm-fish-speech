from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import argparse
import uvicorn
from websocket_handler.exception_handlers import custom_exception_handler
from websocket_handler.websocket_handlers import transcribe 
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception,custom_exception_handler)

@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await transcribe(websocket)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI app with a specified port.")
    parser.add_argument('--port', type=int, default=27000, help='Port number to run the FastAPI app on.')
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)