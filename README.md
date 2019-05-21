# HummingPi

Create a Communication Bridge between the Hummingbird Duo and a Raspberry Pi

## Pre-installation Instructions

- Update your RaspberryPi OS:
```
sudo apt-get update
```
- Upgrade your RaspberryPi OS:
```
sudo apt-get upgrade
```
- Install Java7-jdk
```
sudo apt-get install oracle-java7-jdk
```

## Configure your Hummingbird

WooHoo! You've made it this far. Now let's Configure your Hummingbird!
- Download this repo onto your host computer
- Extract this to your Raspberry Pi's home directory (/home/pi/)
-- The directory link should be `/home/pi/HummingPi/`
- Give permissions to the *Configure* file:
```
chmod +x Configure
```
- Run the Configuration Setup:
```
sudo ./Configure
```
## Configure HummingPi

- Open the *project.config* file and Change the the values:
```
projectType="TYPE OF PROJECT" (Supports java, python)
projectName="NAME OF .JAVA FILE" (ClassTemplate by default)
```
- Give Permissions to *hummingpi.sh*:
```
chmod +x hummingpi.sh
```
## Compiling and Running Java Programs
- Place your .java program with in ./java/src/ (/home/pi/HummingPi/java/src/)
- Run the script (twice if you get a buggy error, that I am trying to fix):
```
sudo ./hummingpi.sh
```

## (Optional) Run project on reboot
- Make a crontab:
```
crontab -e
```
- Select 2 (easiest one @nano)
- Create a new line and add:
```
@reboot sudo /home/pi/HummingPi/relay.sh
```