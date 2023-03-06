This version FAiled for following reason
1. Too many Threads which are inactive , which makes
    - update is not frequent

Installation step 
1. install Anaconda
    - set anaconda as PATH variable so that batch file is usable
        - https://www.geeksforgeeks.org/how-to-setup-anaconda-path-to-environment-variable/
    - run conda init at first time
2. import environemnt and name it as robot using the environment.yaml file
3. install CAM driver and test application (using OV2981 arducam)
    - CAM driver
    - https://github.com/ArduCAM/ArduCAM_USB_Camera_Shield/tree/master/Drivers
    - AMPCAM test
    - https://amcap.en.softonic.com/download
4. install nodeJs (for pymakr)
5. Install pymakr extension
6. install studiono bit driver