import os
import subprocess
import json

def find_usbs():
    try:
        # Run the lsblk command and get the output in JSON format
        result = subprocess.run(['lsblk', '-J'], capture_output=True, text=True, check=True)
        lsblk_output = result.stdout

        # Parse the JSON output
        lsblk_data = json.loads(lsblk_output)

        # List to store USB device info
        usb_devices = []

        # Iterate through the block devices
        for device in lsblk_data['blockdevices']:
            if 'usb' in device.get('tran', '').lower():
                usb_devices.append(
                     device['name']  
                )

        return usb_devices

    except subprocess.CalledProcessError as e:
        print(f"Error executing lsblk: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def check_ext4(usb):
    result = subprocess.run(['df', '-T', '/dev/{usb}'], capture_output=True, text=True, check=True).stdout
    return 'ext4' in result

def mount(usb):
    os.system("mkdir /mnt")
    os.system("mkdir /mnt/usb")
    os.system(f"mount -t ext4 -o rw /dev/{usb} /mnt/usb")

def bmount(usb):
    os.system("cd ~")
    os.system("umount /mnt/usb")
    os.system("umount /")
    os.system("sudo mount /dev/{usb} /")

def umount():
    os.system("cd ~")
    os.system(f"umount /mnt/usb")

def check_correct(usb):
    try:
        mount(usb)
        f = open("/mnt/usb/.is_the_file_system", "r")
        f.close()
        return True
    except:
        umount()
        return False

def create_partition(device):
    try:
        # Check the current partition table and free space
        subprocess.run(['sudo', 'parted', device, 'print', 'free'], check=True)

        # Create a new partition using the remaining space
        subprocess.run(['sudo', 'parted', '-s', device, 'mkpart', 'primary', '0%', '100%'], check=True)

        # Format the new partition (assuming it is the last partition)
        partitions_output = subprocess.run(['lsblk', '-no', 'NAME', device], capture_output=True, text=True)
        partitions = partitions_output.stdout.strip().split('\n')
        new_partition = f"{device}{partitions[-1][-1]}"

        subprocess.run(['sudo', 'mkfs.ext4', new_partition], check=True)

        print(f"New partition {new_partition} created and formatted successfully.")
        return new_partition
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return 0

def sync_data(usb):
    bmount(usb)

def create_default():
    os.system(f"sudo rsync -aAX / /mnt/usb/")
    umount()

def after_load():
    os.system("python3 afterload.py")

def main():
    x = False
    usb_devices = find_usbs()
    for usb in usb_devices:
        if not check_ext4(usb):
            continue
        if not check_correct(usb):
            continue
        x = True
        umount()
        sync_data(usb)
    
    y = False
    if not x:
        for usb_ in usb_devices:
            x = input(f"Make New Partition On To - {usb} ? [Y/n]")
            if x == "n":
                continue

            usb = create_partition(usb_)
            
            if usb != 0:
                y = True
                mount(usb)
                f = open("/mnt/usb/.is_the_file_system", "w")
                f.write("....")
                f.close()
                create_default()
                sync_data(usb)
                break
            else:
                print(f"Failed to make partition on {usb_}")
    if not y:
        print("You havent made a partiton/ You havent connected the USB/ Couldnt Detect the USB/ Couldnt make partition !\n- reloading...")
        main()

    else:
        after_load()

main()
