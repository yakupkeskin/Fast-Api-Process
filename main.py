import get_time
import uvicorn
from fastapi import FastAPI,Request,Form,Body
from fastapi.templating import Jinja2Templates
import requests
from starlette.responses import RedirectResponse
import json
from islem import islem
from get_time import current_time
from multiprocessing import Process
import socket
from proc import proc_api
import time
import psutil

home = FastAPI()
templates = Jinja2Templates(directory="templates")
proc_list = []
islem_result = ""
my_time = ""

@home.get("/")
def main(request:Request):
    exist_list = check_pid()
    return templates.TemplateResponse("home.html", {"request": request,"procs":exist_list,"result":islem_result,"time":my_time})
@home.post("/")
def pos2(request:Request):
    exist_list=check_pid()
    return templates.TemplateResponse("home.html", {"request": request,"procs":exist_list,"result":islem_result,"time":my_time})

def run_time():
    uvicorn.run(current_time, port=9001)


def run_math():
    uvicorn.run(islem, port=9002)


def run_process():
    uvicorn.run(proc_api, port=9003)

def check_port(port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = a_socket.connect_ex(("127.0.0.1", port))
    a_socket.close()
    if result == 0:
        return False
    else:
        return True

def check_pid():
    result = check_port(9003)
    existing_list=[]
    if not result:
        r = requests.get(f"http://127.0.0.1:9003/processcheck")
        existing_list = r.json().get("existing_list")
    return existing_list




@home.post("/{islem}")
def show(request:Request, islem, a: int = Form(...), b: int = Form(...)):
    result = check_port(9002)
    if result:
        p = Process(target=run_math)
        p.start()
        time.sleep(1)
    nums = {"a": a, "b": b}
    r = requests.post(f"http://127.0.0.1:9002/{islem}", json=nums)
    global islem_result
    islem_result = r.json().get("result")
    #return templates.TemplateResponse("home.html", {"request": request,"result":str(r.json().get("result"))})
    return RedirectResponse(url='http://127.0.0.1:9000/')

@home.post("/pro/")
def pro(request: Request, s:int =Form(...)):
    result = check_port(9003)
    if result:
        p = Process(target=run_process)
        p.start()
        time.sleep(1)
    seconds = {"seconds":s}
    r = requests.post(f"http://127.0.0.1:9003/processolustur", json = seconds)
    global proc_list
    proc_list = r.json().get("proc_list")
    return RedirectResponse(url='http://127.0.0.1:9000/')


@home.get("/saatkac")
def saat_kac(request: Request):
    result = check_port(9001)
    if result:
        p = Process(target=run_time)
        p.start()
        time.sleep(1)
    r = requests.get(f"http://127.0.0.1:9001/saatkac")
    global my_time
    my_time = r.json().get("time")
    return RedirectResponse(url='http://127.0.0.1:9000/')
    #return templates.TemplateResponse("home.html", {"request": request,"time":str(r.json().get("time"))})





if __name__ == "__main__":
    uvicorn.run(home,port=9000)

