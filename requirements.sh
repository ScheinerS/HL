sudo apt update
sudo apt upgrade

# Anaconda:
sudo apt install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 -y
#wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
#sha256sum /tmp/Anaconda3-2020.02-Linux-x86_64.sh
#bash /tmp/Anaconda3-2020.02-Linux-x86_64.sh
bash /tmp/Anaconda3-2021.11-Linux-x86_64.sh

# pip3:
sudo apt install python3-pip -y

# openpyxl:
pip3 install openpyxl

# NumPy, SciPy, Matplotlib:
sudo apt install python3-numpy python3-scipy python3-matplotlib

# PanDas:
sudo -H pip3 install pandas
sudo apt install python3-opencv -y

# Spyder:
sudo apt install spyder -y

