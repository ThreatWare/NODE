# ThreatWare NODE
ThreatWare is a platform that is intended to perform network scanning to uncover security vulnerabilities. The platform consists of 3 major components: ThreatWare Backend Server, Scanners and Viewer. This component software is known as ThreatWare NODE which houses the
scanning software on a backend server. The software was designed to run on TurnKey Linux Core v16 which is available here: https://www.turnkeylinux.org/download?file=turnkey-core-16.1-buster-amd64.ova  However it should be capable of running on any Debian install and on most Linux systems without modification.
## Prerequisites

### Git

- A good place to learn about setting up git is [here][git-setup].
- You can find documentation and download git [here][git-home].

### VM Configuration

- Log in to your Linux VM as root and perform the following commands:
```
apt install python3-pip python3-scapy python3-flask-cors xsltproc gcc python3-dev libffi-dev rust sudo nmap
```
- Using the Python installer tool pip3 install the following:
```pip3 install setup-tools
pip3 pyopenssl
pip3 install setup-tools-rust
pip3 install flask
```
•	Because ThreatWare is a service that we wish to run on boot.   A systemd configuration file was created with the following settings.
```
[Unit]
Description=threatware-node
After=network.target

[Service]
User=threatware
WorkingDirectory=/home/threatware/
Environment=FLASK_APP=threatware.py
ExecStart=flask run --cert=adhoc --host 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```
And saved in /etc/systemd/system as threatware-node.service
• Create a threatware account, assign it to the ThreatWare group.  
```
useradd threatware -m
usermod -a -G sudo threatware
```
•	We will need a directory for the ThreatWare modules and a directory for new modules to be uploaded into.  These can be created with:
```
mkdir /home/threatware/modules
mkdir /home/threatware/uploads
```
•	We also give it nopassword sudo access for running low-level tools like scapy by adding the following line to /etc/sudoers
```
threatware ALL=(ALL:ALL) NOPASSWD:ALL
```
•	At this point the server is configured and once our server software is in place we can make it start up on book by invoking:
```
systemctl enable threatware-node.service
```
Now do the following:
```
cd /home/threatware
git clone https://github.com/ThreatWare/NODE.git
```
The server's functionality can be tested by going to the URL
https://<your_server_ip>/1.0/modules/list

If you have done everything correction you should receive a JSON response with the following:
```
{
    "action": "listModules",
    "error": true,
    "result": "Unauthorized Access"
}
```
Now proceed to the installation and configuration of the ThreatWare Viewer

## Notes

- A fully functioning ready-to-use VM appliance is available in the releases section.

- This VM has an active SSH port and a root account with the following password:
```
Threat!Ware
````
- The ThreatWare service was developed as a systemd application and may be brought up and down using the systemd commands

```
systemctl start threatware-node
systemctl stop threatware-node
```
