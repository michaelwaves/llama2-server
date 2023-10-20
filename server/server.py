import time
import copy
import asyncio
import requests

from fastapi import FastAPI, Request
from llama_cpp import Llama
from sse_starlette import EventSourceResponse
# Load the model
print("Loading model...")
llm = Llama(model_path="./llama-2-13b-chat.ggmlv3.q4_1.bin") # change based on the location of models
print("Model loaded!")

app = FastAPI()

@app.get("/llama")
async def llama(request: Request, question:str):
    stream = llm(
        f"""{question}""",
        max_tokens=100,
        stop=["\n", " Q:"],
        stream=True,
    )
    async def async_generator():
        for item in stream:
            yield item
    async def server_sent_events():
        async for item in async_generator():
            if await request.is_disconnected():
                break
            result = copy.deepcopy(item)
            text = result["choices"][0]["text"]
            yield {"data": text}
    return EventSourceResponse(server_sent_events())