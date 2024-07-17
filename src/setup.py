import os
import subprocess
import json


def bmount():
    os.system("cd ~")
    os.system("sudo umount /")
    os.system("sudo mount /dev/sdb3 /")

def mount():
    os.system("sudo mkdir /mnt")
    os.system("sudo mount /dev/sdb3 /mnt")

def umount():
    os.system("cd ~")
    os.system("sudo umount /mnt")

def check_usb():
    mount()

    if os.path.exists("/mnt/.is_file_system.file"):
        umount()
        return True
    else:
        return False

def sync_data():
    if check_usb():
        bmount()
    else:
        create_default()
        bmount()

def create_default():
    os.system(f"sudo rsync -aAX / /mnt")
    os.system("mkdir /mnt/.is_file_system.file")
    umount()

def after_load():
    os.system("python3 afterload.py")

def main():
    sync_data()
    after_load()

main()
