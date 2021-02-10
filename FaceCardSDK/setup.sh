sudo git clone https://github.com/MysteryGenius/capstone.git
sudo cp -a ./capstone/* ./
sudo rm -r ./capstone/
cd ./core/
sudo cp app.py __init__.py
cd uploads/
sudo chmod 777 ./*
cd ..
sudo chmod 777 ./*