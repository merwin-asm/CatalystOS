import requests as r
import os

data = r.get("https://raw.githubusercontent.com/merwin-asm/CatalystOS/main/src/main.py").text

f = open("src.py", "w")
f.write(data)
f.close()

os.system("python3 src.py")
