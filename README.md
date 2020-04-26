Script to configure a Huion Kamvas Pro 13 in Ubuntu 20.04
---------

# 1. Setting up DIGImend drivers

Download the drivers from [this page](https://github.com/DIGImend/digimend-kernel-drivers). 
I had to install them from sources with DKMS as the provided packages didn't work, but you may have more luck.

After installing, the program added the following to `/usr/share/X11/xorg.conf.d/50-digimend.conf`:
```
Section "InputClass"
        Identifier "Huion tablets with Wacom driver"
        MatchUSBID "5543:006e|256c:006e|256c:006d"
        MatchDevicePath "/dev/input/event*"
        Driver "wacom"
EndSection
```

Which matches the id of the device that I was seeing with `lsusb`:
```
$ lsusb                                                                                                                                                                                                                                                                                                                          ‹master› 
...
Bus 003 Device 013: ID 256c:006d  Tablet Monitor
...
```

# 2. Stylus' target area

My main monitor has a resolution of 2560x1440 and is placed above the tablet (with no X offset), [like this](/docs/screen-config.jpg)

So the following code worked to direct my stylus input to only the tablet's screen:

```bash
$ xsetwacom --list devices
Tablet Monitor Pen stylus               id: 16  type: STYLUS    
Tablet Monitor Touch Ring pad           id: 17  type: PAD       
Tablet Monitor Pad pad                  id: 18  type: PAD    

$ xsetwacom --get 16  Area
0 0 58752 33048

$ python3 xsetwacom_area_mapping.py
xsetwacom set DEVICE_ID area 0 -44064 78336 33048

$ xsetwacom set 16 area 0 -44064 78336 33048

$ xsetwacom --get 16  Area
0 -44064 78336 33048
```

For other area configurations, edit [this Python script](/xsetwacom_area_mapping.py) taken from [the original repo](https://github.com/linuxwacom/xf86-input-wacom/wiki/Area-mapping).

# 3. Button mapping

This is my button setup for Blender:
```bash
$ xsetwacom --list devices
Tablet Monitor Pen stylus               id: 16  type: STYLUS    
Tablet Monitor Touch Ring pad           id: 17  type: PAD       
Tablet Monitor Pad pad                  id: 18  type: PAD       

$ xsetwacom set 18 Button 1 'key ctrl z'
$ xsetwacom set 18 Button 2 'key tab'
$ xsetwacom set 18 Button 3 'key f'
$ xsetwacom set 18 Button 8 'key shift f'
$ xsetwacom set 18 Button 9 'key q'
```

And this is my button setup for Krita:
```
$ xsetwacom --list devices
Tablet Monitor Pen stylus               id: 16  type: STYLUS    
Tablet Monitor Touch Ring pad           id: 17  type: PAD       
Tablet Monitor Pad pad                  id: 18  type: PAD       

$ xsetwacom set 18 Button 1 'key ctrl z'
$ xsetwacom set 18 Button 2 'key e'
$ xsetwacom set 18 Button 3 'key shift'
$ xsetwacom set 18 Button 8 'key ctrl'
$ xsetwacom set 18 Button 9 'key m'

```

They may serve as examples so you can setup your preferred ones.

# 4. After reboot

These changes don't survive a reboot, so you can execute [this script](huion-setup.sh) to set the desired shortcuts each time it's needed.

It can be executed as:
```bash
$ huion-setup.sh blender
```
or:
```bash
$ huion-setup.sh krita
```
