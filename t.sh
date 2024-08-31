
git clone https://github.com/solus-project/budgie-desktop.git 
cd budgie-desktop
meson build --prefix=/usr/local 
ninja -C build 
ninja -C build install

echo '# Custom Commands' > ~/.xinitrc
echo 'echo command1' >> ~/.xinitrc 
echo '# Start Budgie' >> ~/.xinitrc
echo 'exec budgie-desktop' >> ~/.xinitrc
