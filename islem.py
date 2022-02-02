import uvicorn
from fastapi import FastAPI,Request,Body
from fastapi.templating import Jinja2Templates
import json


islem = FastAPI()
templates = Jinja2Templates(directory="templates")


@islem.post("/{islem}")
async def proc(islem, body:dict=Body(...)):
    res = 0
    a = body.get("a")
    b = body.get("b")

    if islem == "topla":
        res = a+b

    elif islem == "cikar":
        res = a-b

    elif islem == "carp":
        res = a*b

    elif islem == "bol":
        res = a/b

    elif islem == "ustal":
        res = a**b

    return {"result": res}


if __name__ == "__proc__":
    uvicorn.run()