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

d = input("USB DRIVE IS  (/dev/sdb [default] , /dev/sdc.. ): ")
if d == "":
    device = '/dev/sdb'
elif d.endswith("a"):
    print(f"{d} cant be used!!!")
    quit()
else:
    device = d

size = get_usb_size(device)

if size is not None:
    size_mb = int(size / (1024**2))
    size_mb -= 5000
    print(size_mb)
    
    if size_mb < 1000:
        print("Insufficient Space...")

    if not os.path.exists('ventoy'):
        print("Downloading Ventoy")
        os.system("wget https://github.com/ventoy/Ventoy/releases/download/v1.0.99/ventoy-1.0.99-linux.tar.gz -O ventoy.tar.gz")
        os.system("tar -xzvf ventoy.tar.gz")
        os.system("rm ventoy.tar.gz")

    print(f"Installing Ventoy on {device}")
    os.system(f"sudo ./ventoy/Ventoy2Disk.sh -i {device} -r {size_mb} -L CatalystOS -I")
    
    print(f"Making {device}3 Partition : {size_mb}")
    e_size = get_usb_size(f'{device}1') + get_usb_size(f'{device}2')
    e_size = int(e_size / (1024**2)) + 1000
    os.system(f"sudo parted {device} --script mkpart primary ext4 {e_size}MB 100%")
    
    print(f"Making ext4 filesystem for {device}3")
    os.system(f"sudo mkfs.ext4 -F {device}3")
    
    print("Copying files to USB")

    c = [
            "sudo mkdir /mnt/usb",
            f"sudo mount {device}1 /mnt/usb",
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
