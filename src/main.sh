sudo pacman-key --init --noconfirm
sudo pacman-key --populate archlinux --noconfirm
sudo pacman -Syu --noconfirm
pip install -r requirements.txt
clear
python3 main.py
