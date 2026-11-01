# Installation instructions

Note that this code is designed to run on a Respeaker Core 1.0 that has reached EOL and runs an old Python 2.7.9.
Note the ssh command for this device: `ssh -o HostKeyAlgorithms=+ssh-rsa root@<IP>`.

1. Copy all files in this directory to the ReSpeaker under `/root/`
2. Install the customised Python library:
   ```
   cd /root/respeaker_python_library 
   pip install .
   ```
3. Set up recording to start automatically after boot:
   ```
   cp /root/record /etc/init.d/
   chmod +x /etc/init.d/record
   /etc/init.d/record enable
   /etc/init.d/mopidy disable
   ```
4. Reboot