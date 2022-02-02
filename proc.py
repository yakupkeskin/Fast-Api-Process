import time
import psutil
import uvicorn
from fastapi import FastAPI,Request,Body
from fastapi.templating import Jinja2Templates
import datetime
from multiprocessing import Process
from fastapi.responses import RedirectResponse
proc_api = FastAPI()
templates = Jinja2Templates(directory="templates")
proc_list = []

def new_proc(seconds):
    print(f"started sleeping for {seconds} seconds")
    time.sleep(seconds)
    print('Done Sleeping')
    return ""


@proc_api.post("/processolustur")
async def proc(body:dict=Body(...)):
    global proc_list
    seconds = body.get("seconds")
    p = Process(target=new_proc, args=[seconds])
    p.start()
    pd = p.pid
    proc_dict = {"pid":pd,"seconds":seconds}
    proc_list.append(proc_dict.copy())
    return {"proc_list":proc_list}


@proc_api.get("/processcheck")
def processcheck():
    global proc_list
    existing_list = []
    p = Process(target=new_proc, args=[0])
    p.start()
    p.join()
    for proc in proc_list:
        if psutil.pid_exists(proc["pid"]):
            existing_list.append(proc)
    proc_list = existing_list
    return {"existing_list":existing_list}

