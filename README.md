
# Guide to setup the Hardware.

1. [Introduction](1)
2. [Hardware and Software Requirements List]()
3. [Hardware/Softwares installation]()
4. [Configuration]()
5. [Error_Handling]()


# Introduction

This prototype was developed by __Roadlytics__ inorder to generate data of Logistic/Delivery Vehicles to spot the parking hotspots in the city of Hamburg. The aim of this project is to collect our own **Geo Spatial Data** for tackling traffic congested related projects in the city of hamburg, further down we integrate this data with other available data to solve different city planning problems. Our team is developing a portable device based on *__GNSS__* (Global Navigation Satellite System) equipped on top of __Raspberry pi ZERO__ and a __Battery module__ with the capability of detect the position of the vehicle with high accuracy and low error rate. Some of the other analysis we will carry out in this project are:

+ Main delivery zones
+ Critical parking hotspots
+ Position of the vehicles (if parking at the second row, bike lane, etc.)
+ Most congested periods of time
+ Most frequented routes

User can use our tool to look for different information by selecting options available on teh left pane of the dashboard, some of the options would be :

+ Selections of the Districts in Hamburg
+ Time frame selection 
+ Hotspot Selection...

# Hardware and Software Requirements List

## Things used in this project

+ [Raspberry Pi Zero](https://www.raspberrypi.org/products/raspberry-pi-zero/?resellerType=home)
+ [Ublox - GNSS Module](https://www.mikroe.com/gnss-4-click)
+ [Battery Hat](https://www.waveshare.com/li-ion-battery-hat.htm)
+ [SD Card](https://www.conrad.de/de/o/sd-karten-0412021.html)
+ [Jumper Wires](https://www.conrad.de/de/search.html?search=jump%20wire&searchBarInput=wires)
+ [Raspbian OS](https://www.raspberrypi.org/downloads/raspberry-pi-os/)


# Softwares installation

## Assembling Hardware

	1. Insert SD card into PI's SD card slot, solder 4 pins on PI
		* Tx for data transmission
		* Rx for data receiving
		* VCC for power supply
		* GND for ground
	2. fix the Battery Module on top of raspberry pi, make sure the above 4 pins are intackt with teh same 4 pins of battery module, screw the 4 corners.
	3. using Jumper female to female wires, make the connection with GNSS receiver
		* PINS form Battery Hat  --> PINS to Receiver
		
|Battery Hat| GNSS receiver |
| -------- |:-------------:|
| Tx PIN      | Rx PIN |
| Rx PIN     | Tx PIN      |
| VCC power supply | 3V power supply     |
| GND	| GND 	|


	4. Insert 14500 lithium battery in the battery hat, once all the above steps followed we are good to switch on the device, once switching ON, all the light glows which is teh indication for device is ON
		it takes approx 1-minute to get GPS fix based on the outdoor condition, once the receiver gets fix data it starts glowing ORANGE light


## in case of __Headless PI__(without External Monitor) follow the below steps

1. Install Raspberry PI Operating System on an SD Card, to make the process quick use RPI-imager tool, more details of the tool can be found [here](https://www.raspberrypi.org/documentation/installation/installing-images/)
To install it on linux machine please run the below command
   		
	*		```
  		 	sudo apt install rpi-imager
	   		```

2. Once an image is created on an SD card, by inserting it into a card reader on a Linux or Windows machines the **boot folder and root folder** can be accessed. Adding certain files to this folder will activate certain setup features on the first boot of the Pi itself.

3. Add “SSH” File to the SD Card **Root folder** : Enable SSH by placing a file named “ssh” (without any extension) onto the boot partition of the SD card
4. edit config.txt
            #add new line to enable uart communication
            enable_uart=1

4. to setup wireless networking: Add "wpa_supplicant.conf" in **Boot folder**
	
	*					
			
			ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
			update_config=1
			country=<DE

			network={
 			ssid="<Name of your wireless LAN>"
 			psk="<Password for your wireless LAN>"
			}
			
5. after the above steps, please insert the SD card in raspberry pi and 'power on' the device, it will take few minutes to boot - first installation/boot.
6. on your phone, install 'Network IP Scanner', you have to be in the same network as raspberry pi , then open the app and hit scan, note down the IP Address of the PI
7. ssh pi with it's IP (we have got the IP from above step #6) using default credentails with PuTTY

		username : pi
		password: raspberry
		
		
7. After first time login, enable __serial port communication__
		
	*		```
			sudo raspi-config
			```
	+ select option [5] and enable serial port 
8. We can check if we are able to receive serial data by below command
		*	
			```
			sudo cat /dev/ttyAMA0
			or
			sudo cat /dev/Serial0
			or
			sudo cat /dev/S0
			```

# Configuration: Dependencies have to be installed in the Raspberry Pi

## run the below commands on pi's terminal
	
*	```
		sudo apt-get update |
		sudo apt-get upgrade |
		sudo apt-get install pip3 |
		sudo pip3 install pynmea2 |
		sudo pip3 install pyserial
	```
	
* **"sudo python3 /home/pi/Desktop/tracker_sourceCode.py & > /home/pi/Desktop/startupscript.log &"**
	add the above line to __**/etc/rc.local**__ to auto start the script whenver there is a boot happens.
	Make sure the rc.local script is executable : sudo chmod +x /etc/rc.local
	Then enable : sudo systemctl enable rc-local.service
	Reboot the system or start the script manually by running: sudo systemctl start  rc-local.service
	The service status can be displayed by running: sudo systemctl status  rc-local.service
	 
	
# Error Handling

### How to setup Static IP Address for Raspberry PI

* Notedown current IP Address of Raspberry Pi (in our case it is connected to wifi hence we will notedown 'wlan0' ip address that is 10.29.244.XXX)
	** command to check the IP address is 'ifconfig'
* Notedown router gateway address
	** command to check the routers gateway address is 'sudo route -n' in our case it was 10.29.244.1
* edit the file with below information __**'/etc/dhcpcd.conf'**__

		sudo nano /etc/dhcpcd.conf
		interface wlan0
		static ip_address=10.29.244.100
		static routers=10.29.244.1
		static domain_name_servers=8.8.8.8 8.8.4.4

* once you update the above file, sudo reboot and you will able to connect your pi with above setted static IP.

### How to solve the error encounter in NMEA sentences $GPTXT,01,01,01,NMEA unknown msg*58 or $GPTXT,01,01,01,NMEA unknown msg*46

* Check your serial port configuration. If the 'echo' option is enabled that will cause this problem. in Linux you can do *'stty -F /dev/ttyS1 -echo'* to disable echo then cat the gps serial device and those messages should stop.
