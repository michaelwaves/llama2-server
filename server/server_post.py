from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/llama")
async def llama(question: str = Form(...)):
    stream = llm(
        f"""{question}""",
        max_tokens=100,
        stop=["\n", " Q:"],
        stream=True,
    )
    # Process the stream or return the response as needed
    # ...
    return {"question": question, "response": stream}