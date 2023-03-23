# boot.py -- run on boot-up
import json
f = open('config.json')
config = json.load(f)
id = config['arID']
print('This is ',id)
# downloadMode = config["DownloadMode"]
# f.close()
# print('downloadMode:',downloadMode)
# if downloadMode:
#     print('opening other python script...')
#     scriptFile = "downloadAndRun.py"
#     with open(scriptFile,mode='r',encoding="utf-8")as f:
#         code = f.read()   
#     print("read py")
#     print(f)
#     exec(code)
#     # with open (scriptFile,"r") as f:
#     #     scrptContent = f.read()
#     # exec()
# print("[boot]]Running boot script from Robot ",id)
from utime import sleep_ms