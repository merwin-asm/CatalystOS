import subprocess
import os

def get_usb_size(device):
    try:
        result = subprocess.run(['lsblk', '-b', '-o', 'SIZE', device], 
                                capture_output=True, text=True, check=True)
        size = result.stdout.split('\n')[1].strip()
        return int(size)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing command: {e}")
    except IndexError:
        print("Device not found.")
    except ValueError:
        print("Invalid size format.")
    return None

input("Remove all USB connected (if any) then press enter ! : ")

device = '/dev/sdb'
size = get_usb_size(device)

if size is not None:
    size_mb = int(size_bytes) / (1024**2)
    size_mb -= 2000
    
    if size_mb < 1000:
        print("Insufficient Space...")

    if not os.path.exists('ventoy'):
        print("Downloading Ventoy")
        os.system("wget https://github.com/ventoy/Ventoy/releases/download/v1.0.99/ventoy-1.0.99-linux.tar.gz -O ventoy.tar.gz")
        os.system("tar -xzvf ventoy.tar.gz")
        os.system("rm ventoy.tar.gz")

    print("Installing Ventoy on /dev/sdb")
    os.system(f"sudo ./ventoy/Ventoy2Disk.sh -i /dev/sdb -r {size_mb} -L CatalystOS -I")
    
    print(f"Making /dev/sdb3 Partition : {size_mb}")
    os.system("sudo parted /dev/sdb --script mklabel msdos")
    os.system(f"sudo parted /dev/sdb --script mkpart primary ext4 0% {size_mb}MB")
    
    print("Making ext4 filesystem for /dev/sdb3")
    os.system("sudo mkfs.ext4 -F /dev/sdb3")
    
    print("Copying files to USB")

    c = [
            "sudo mkdir /mnt/usb",
            "sudo mount /dev/sdb1 /mnt/usb",
            "sudo cp catalystos.iso /mnt/usb/catalystos.iso",
            "sudo mkdir /mnt/usb/ventoy",
            "sudo cp ventoy.json /mnt/usb/ventoy/ventoy.json",
            "sudo umount /mnt/usb"
    ]

    for e in c:
        os.system(e)
    
    print("Done installing CatalystOS!!")

else:
    print("USB Not Found...")
