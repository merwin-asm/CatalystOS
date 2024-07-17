import subprocess
import re

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr, result.returncode

def get_partition_table(device):
    command = f"sudo parted -s {device} unit s print"
    stdout, stderr, returncode = run_command(command)
    if returncode != 0:
        raise RuntimeError(f"Failed to get partition table: {stderr}")
    return stdout

def get_partition_info(partition_table, partition_number):
    lines = partition_table.splitlines()
    header = lines[0]
    partitions = lines[2:-2]  # Exclude header and last two lines (units and free space)

    # Find the line for the specific partition number
    for line in partitions:
        if line.startswith(f" {partition_number}"):
            return line.strip().split()

    return None

def resize_partition(device, partition_number, new_size):
    command = f"sudo parted -s {device} resizepart {partition_number} {new_size}"
    stdout, stderr, returncode = run_command(command)
    if returncode != 0:
        raise RuntimeError(f"Failed to resize partition {partition_number}: {stderr}")

def move_partition(device, partition_number, new_start):
    command = f"sudo parted -s {device} move {partition_number} {new_start}"
    stdout, stderr, returncode = run_command(command)
    if returncode != 0:
        raise RuntimeError(f"Failed to move partition {partition_number}: {stderr}")


def resize_filesystem(device, partition):
    filesystem_type = detect_filesystem(device + str(partition))
    
    if filesystem_type == "ext2" or filesystem_type == "ext3" or filesystem_type == "ext4":
        command = f"sudo resize2fs {device}{partition}"
    elif filesystem_type == "xfs":
        command = f"sudo xfs_growfs {device}{partition}"
    elif filesystem_type == "ntfs":
        command = f"sudo ntfsresize -f {device}{partition}"
    elif filesystem_type == "fat16":
        command = f"sudo fatresize -s {device}{partition}"
    elif filesystem_type == "fat32":
        command = f"sudo fatresize -s {device}{partition}"
    elif filesystem_type == "no filesystem":
        # If there's no filesystem, skip resizing
        print(f"No filesystem detected on {device}{partition}, skipping resize.")
        return
    else:
        raise NotImplementedError(f"Filesystem type {filesystem_type} not supported.")
    
    stdout, stderr, returncode = run_command(command)
    if returncode != 0:
        raise RuntimeError(f"Failed to resize filesystem on {device}{partition}: {stderr}")

def detect_filesystem(partition_device):
    command = f"sudo blkid -o value -s TYPE {partition_device}"
    stdout, stderr, returncode = run_command(command)
    if returncode != 0:
        # If blkid fails to detect, check if it's a recognized filesystem
        if re.search(r"No such file or directory", stderr):
            return "no filesystem"
        else:
            raise RuntimeError(f"Failed to detect filesystem type for {partition_device}: {stderr}")
    return stdout.strip()

def main():
    usb_device = "/dev/sdb"

    try:
        partition_table = get_partition_table(usb_device)

        partition_info = get_partition_info(partition_table, 1)
        if partition_info:
            current_start = partition_info[1]
            new_start = "2GB"
            resize_partition(usb_device, 1, new_start)
            move_partition(usb_device, 1, new_start)
            resize_filesystem(usb_device, 1)

        partition_info = get_partition_info(partition_table, 2)
        if partition_info:
            current_start = partition_info[1]
            current_end = partition_info[2]
            new_start = f"{int(current_end) + 50 * 1024 * 1024 // 512}s"
            resize_partition(usb_device, 2, new_start)
            move_partition(usb_device, 2, new_start)
            resize_filesystem(usb_device, 2)

        partition_info = get_partition_info(partition_table, 3)
        if partition_info:
            current_end = partition_info[2]
            new_end = "100%"
            resize_partition(usb_device, 3, new_end)
            move_partition(usb_device, 3, new_end)
            resize_filesystem(usb_device, 3)

        print("Partition resizing and moving completed successfully!")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
