from pathlib import Path
from bs4 import BeautifulSoup
import requests
import os
from colorama import Fore , init
import shutil
import ast
import platform
sistema_operativo = platform.system()
from pyshortext import unshort

if sistema_operativo == "Windows":
    cmd = "cls"
elif sistema_operativo == "Linux":
    cmd = "clear"

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def progress(filename,index,total):
    ifmt = sizeof_fmt(index)
    tfmt = sizeof_fmt(total)
    printl(f'{filename} {ifmt}/{tfmt}')
    pass

def printl(text):
    init()
    print(Fore.GREEN + text,end='\r')

def make_session(dl):
    session = requests.Session()
    username = unshort(dl['u'])
    password = unshort(dl['p'])
    host = unshort(dl['h'])
    url = host+"login/index.php"
    resp = session.get(url,allow_redirects=True,verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    token = soup.find("input", attrs={"name": "logintoken"})["value"]
    payload = {
        "logintoken": token,
        "username": username,
        "password": password
    }
    resp = session.post(url,data=payload,verify=False)
    return session

def wait_download(url,ichunk=0,index=0,file=None,session=None):
    init()
    printl(Fore.RED + 'Iniciando sesion!!!')
    dl = url
    filename = dl['fn']
    total_size = dl['fs']

    if not session:
        session = make_session(dl)    
    if session:
        init()
        os.system(cmd)
        printl(Fore.BLUE + 'Sesion Iniciada ... !!!')
    else:
        init()
        os.system(cmd)
        printl(Fore.RED + 'Error al iniciar sesion ... !!!')
    dl["urls"] = unshort(dl["urls"]).split("\n")
    state = 'ok'
    i = ichunk
    l = 1
    j = str(l)
    chunk_por = index
    filet = 'Downloading: ' + dl['fn']
    filename = dl['fn']
    if os.path.exists(filename):
        os.unlink(filename)
    if len(filet) > 30:
        filet = 'Downloading ... '
    f = open(filename,"wb") 
    os.system(cmd)
    while total_size > chunk_por: 
        chunkurl = dl['urls'][i]
        resp = session.get(chunkurl,stream=True,verify=False)  
        for chunk in resp.iter_content(chunk_size=1024*256):
            chunk_por += len(chunk)
            f.write(chunk)
            progress(f'{filet} ',chunk_por,total_size)
        l+=1
        i+=1
    f.close()
    if os.path.exists('Downloads_C/' + filename):
        os.unlink('Downloads_C/' + filename)
    shutil.move(filename,'Downloads_C/'+filename)
        
    os.system(cmd)
    printl('Descarga Finalizada !!! Archivos Guardados en ./Downloads. Envie 0 y luego Enter para salir o pulse solo Enter para continuar')
    state = 'finish'
    a = input()
    if a == '0':
        if state == 'finish':
            return False,i,chunk_por,file,session
    else:
        return True,i,chunk_por,file,session

def initi():
    while (True):
        ichunk = 0
        index = 0
        file = None
        session = None
        init()
        print(Fore.CYAN + 'Pegue una direct Url')
        msg = input()
        url = ast.literal_eval(msg)
        if os.path.exists('Downloads_C/'):
            pass
        else:
            os.mkdir('Downloads_C/')
        wait,ichunk,index,file,session = wait_download(url,ichunk,index,file,session)
        if not wait:
            break
    
if __name__ == '__main__':
    initi()