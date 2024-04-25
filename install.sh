# Install dependencies for pyspacemouse and configure
# sudo apt-get install libhidapi-dev

# Manually make this file
sudo echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' > /etc/udev/rules.d/99-hidraw-permissions.rules
sudo usermod -aG plugdev $USER
newgrp plugdev

sudo apt-get install sense-hat