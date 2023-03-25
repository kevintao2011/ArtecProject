# Installation steps
1. Install Node.js
2. Install pymakr
3. get Studuinobit micoropython bin file
4. Install esptool using pip install and erase with command
    - esptool.py --chip esp32 --port COM10 erase_flash
5. run esptool.py --chip esp32 --port COM3 --baud 1500000 write_flash -z 0x1000 sbmp-20190830-v0.9.8.bin to flash firmware 
    - download link :https://www.artec-kk.co.jp/artecrobo2/data/sbmp-20190830-v0.9.8.bin
6. run 


this system heavily rely on micropython socket library, see this reference for details:
    -https://docs.micropython.org/en/latest/library/socket.html
