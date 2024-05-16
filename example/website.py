from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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
