# Hardware installation
To get the NFC cube running, you have to patch the list of known card
readers on your system. Due to system integrity constraints I was not
able to do this on my MacBook Pro.

Solution was to spin up a Ubuntu VM in VirtualBox and give it access to
 the USB port.

On the VM, a few additional packages are required:
```
sudo apt-get install libccid pcscd libpcsclite1 pcsc-tools swig
libpcsclite-dev
```

Copy the `Info.plist.patch` on the VM and run
`path /usr/lib/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist
Info.plist.patch` to patch the list of known card readers.

# Software instructions
The software is implemented in python3. Run the usual `pip3 install -y
 -t requirements.txt` to get all dependencies installed.

# Run it
Finally, run the code by calling `python cardreader.py`.