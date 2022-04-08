# NmapEmail

## Scan with nmap and send a mail if a new port is open.

### Install:
cd /usr/src

git clone https://github.com/teknoprep/NmapScan.git
apt install nmap xsltproc


Nmap needs to be installed. (*apt install nmap* on Ubuntu/Debian systems)
Sender_email, receiver_email and password needs to be added in **def mail**.

### To use
To use start with **python3 nmap_email.py -new *ip address to scan*** to make a template.
To compare template with a new scan run **python3 nmap_email.py -ip *ip address to scan***

In **def nmap** you can change the syntax used with nmap.

### Cron Job
0 10 1 * *  python3 /usr/src/nmapemail/nmap_email.py -new 192.168.111.1-254
