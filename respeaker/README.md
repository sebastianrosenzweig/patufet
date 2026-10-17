# Installation instructions

1. Copy all files in this directory to the ReSpeaker under `~/`
2. Install the customised Python library:
   ```
   cd ~/respeaker_python_library 
   pip install .
   ```
3. Set up recording to start automatically after boot:
   ```
   cp /root/record /etc/init.d/
   chmod +x /etc/init.d/record
   /etc/init.d/record enable
   ```
4. Reboot