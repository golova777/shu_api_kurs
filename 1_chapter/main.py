from fastapi import FastAPI, Query, Body
from fastapi.responses import FileResponse
import uvicorn
from starlette.staticfiles import StaticFiles

from hotels import router as router_hotels



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_hotels)

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
    return FileResponse("static/favicon.ico")


@app.get('/', summary="просто стартовая", description="описание сложной бизнес логиги")
def func():
    return {'hello': 'world!!!fffff'}



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)