import time
import os

try:
  f = open("/etc/os-settings.json")
except:
  os.system("sudo pacman -S archinstall")
  os.system("archinstall")
  f = open("/etc/os-settings.json", "w")
  f.write({})
  f.close()

while True:
  print("HELLO")
  time.sleep(2)
