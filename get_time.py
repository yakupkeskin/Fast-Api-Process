import uvicorn
from fastapi import FastAPI,Request,Body
from fastapi.templating import Jinja2Templates
import datetime

current_time = FastAPI()
templates = Jinja2Templates(directory="templates")


@current_time.get("/saatkac")
async def proc():
    now = datetime.datetime.now()
    time = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    return {"time":time}
