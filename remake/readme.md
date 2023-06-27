#   Required folder
    - Server : Server4.py
    - Object Dectect porgram: cameraNew.py
    - Command line interface: clientRemakeNew.py
    

#   Recommended development environment
This project is developed using extenstions and Visaul Studio Code and on Windows system. It is recommended to follow same setup for better development experience. The setup guide is provided below

#   Installation guide
1. Install Anaconda
    - set anaconda as PATH variable so that batch file is usable
        - https://www.geeksforgeeks.org/how-to-setup-anaconda-path-to-environment-variable/
    - run conda init at first time
2. Import environemnt and name it as robot using the environment.yaml file
3. Install CAM driver and test application (using OV2981 arducam)
    - CAM driver
    - https://github.com/ArduCAM/ArduCAM_USB_Camera_Shield/tree/master/Drivers
    - AMPCAM test
    - https://amcap.en.softonic.com/download
4.  Install nodeJs (for pymakr)
    - official website https://nodejs.org/en
5. Install pymakr extension on Visual Studio
    - https://alepycom.gitbooks.io/pycom-documentation/content/chapter/pymakr/installation/vscode.html
6.  Install studiono bit driver
    - offical website https://www.artec-kk.co.jp/artecrobo2/en/software/
# Firmware for ArtecRobo2
3. get Studuinobit micoropython bin file 
    - download link :https://www.artec-kk.co.jp/artecrobo2/data/sbmp-20190830-v0.9.8.bin
4. Install esptool using pip install and erase with command
    - esptool.py --chip esp32 --port COM10 erase_flash
5. run esptool.py --chip esp32 --port COM3 --baud 1500000 write_flash -z 0x1000 sbmp-20190830-v0.9.8.bin to flash firmware 

# Libraries
This system heavily rely on openCV and library of ArtecRobo and Python socket, see these references for details:
    -https://docs.micropython.org/en/latest/library/socket.html
    -https://github.com/artec-kk/StuduinoBit_MicroPython
    -https://docs.micropython.org/en/latest/esp32/quickref.html
    -https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
