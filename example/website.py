import time
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from chat_buy.api.models import Message

app = FastAPI()

# Подключение статических файлов
app.mount("/styles", StaticFiles(directory="./example/static/styles"), name="styles")
app.mount("/scripts", StaticFiles(directory="./example/static/scripts"), name="scripts")


@app.get("/")
async def index():
    """
    Returns html-page with chat window.
    """
    return FileResponse("./example/templates/index.html")

@app.post("/v1/chat/")
async def process_messages(messages: list[Message]) -> StreamingResponse:
    """
    Processes a list of messages and streams back a response.
    """

    def getter(x):
        time.sleep(0.05)
        return x
    
    return StreamingResponse(
        (getter(product) for product in ["молоток", "Гвозди", "Хлеб", "Дайкон"]),
        media_type="text/event-stream",
        headers={"Response-Agent": "SearchQueryAgent"},
    )


from chat_buy.agents import search_query_agent
from chat_buy.api.models import Product


@app.post("/v1/provision/")
async def process_provision(product: Product) -> dict:
    """
    Searches for product information on marketplaces and returns results to the user.
    Returns dictionary with keys: link, name, price, photo.
    """
    return {"link1": "https://www.google.com/search?channel=fs&client=ubuntu-sn&q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA",
            "link2": "https://www.google.com/search?channel=fs&client=ubuntu-sn&q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA",
            "link3": "https://www.google.com/search?channel=fs&client=ubuntu-sn&q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA"}
            