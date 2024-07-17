#!/bin/bash


echo "Please remove all USB devices except the one you want to work with."
read -r

if [ ! -d "ventoy" ]; then
    echo "Downloading Ventoy..."
    wget https://github.com/ventoy/Ventoy/releases/download/v1.0.99/ventoy-1.0.99-linux.tar.gz -O ventoy.tar.gz
    
    tar -xzvf ventoy.tar.gz
    
    rm ventoy.tar.gz
    
    echo "Ventoy has been downloaded and extracted."
else
    echo "Ventoy directory already exists. Skipping download."
fi

echo "Installing ventoy on USB.."
sudo ./ventoy/Ventoy2Disk.sh -i /dev/sdb

echo "Adding catalystos.iso and ventoy.json...."
sudo mkdir /mnt/usb
sudo mount /dev/sdb1 /mnt/usb
sudo cp catalystos.iso /mnt/usb/catalystos.iso
sudo mkdir /mnt/usb/ventoy
sudo cp ventoy.json /mnt/usb/ventoy/ventoy.json
sudo umount /mnt/usb

echo "Editing partitions END START SIZE etc........."
python3 setup_usb.py

echo "INFO:"
echo "--sdb"
echo "------sdb1 (primary) contains the ISO" 
echo "------sdb2 (primary) contains ventoy files"
echo "------sdb3 (primary) Where you will store your files in the OS"
echo "DONE!!"
