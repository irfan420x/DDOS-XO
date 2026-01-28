#!/bin/bash
# WORMGPT KALI LINUX AUTO INSTALLER - FIXED VERSION
# Run: sudo ./install.sh

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║           WORMGPT KALI NUCLEAR INSTALLER v5.0           ║"
echo "║              ALL-IN-ONE ATTACK SOLUTION                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check root
if [[ $EUID -ne 0 ]]; then
   echo "[!] Run as root: sudo $0"
   exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[+] Phase 1: System Update${NC}"
apt-get update -y
apt-get upgrade -y
apt-get dist-upgrade -y

echo -e "${GREEN}[+] Phase 2: Installing Tools${NC}"
apt-get install -y \
    python3 python3-pip python3-dev \
    tor proxychains4 privoxy \
    nmap whatweb nikto dirb gobuster \
    slowhttptest goldeneye hping3 \
    masscan dnsutils net-tools \
    git wget curl axel \
    build-essential libssl-dev libffi-dev \
    chromium chromium-driver \
    screen tmux htop iftop \
    nodejs npm > /dev/null 2>&1

echo -e "${GREEN}[+] Phase 3: Python Packages${NC}"
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo -e "${GREEN}[+] Phase 4: TOR Configuration${NC}"
systemctl stop tor
cat > /etc/tor/torrc << 'EOF'
SocksPort 9050
SocksPort 9052
ControlPort 9051
CookieAuthentication 1
Log notice file /var/log/tor/notices.log
DataDirectory /var/lib/tor
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:80
LongLivedPorts 80,443
EOF
systemctl start tor
systemctl enable tor

echo -e "${GREEN}[+] Phase 5: Proxy Setup${NC}"
cat > /etc/proxychains4.conf << 'EOF'
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
localnet 127.0.0.0/255.0.0.0
quiet_mode

[ProxyList]
socks5 127.0.0.1 9050
socks5 127.0.0.1 9052
http 127.0.0.1 8118
EOF

echo -e "${GREEN}[+] Phase 6: Creating Attack Directory${NC}"
mkdir -p /opt/wormgpt
cp wormgpt_main.py /opt/wormgpt/ 2>/dev/null || true
cp config.json /opt/wormgpt/ 2>/dev/null || true
cp requirements.txt /opt/wormgpt/ 2>/dev/null || true
chmod +x /opt/wormgpt/wormgpt_main.py 2>/dev/null || true

echo -e "${GREEN}[+] Phase 7: Creating Desktop Shortcut${NC}"
cat > /usr/share/applications/wormgpt.desktop << EOF
[Desktop Entry]
Name=WORMGPT Nuclear
Comment=All-in-One DDoS Attack Tool
Exec=python3 /opt/wormgpt/wormgpt_main.py
Icon=/usr/share/icons/gnome/256x256/apps/utilities-terminal.png
Terminal=true
Type=Application
Categories=Utility;Security;
EOF

echo -e "${GREEN}[+] Phase 8: Setting Aliases${NC}"
echo "alias wormgpt='cd /opt/wormgpt && python3 wormgpt_main.py'" >> ~/.bashrc
echo "alias wormstart='systemctl start tor && proxychains python3 /opt/wormgpt/wormgpt_main.py'" >> ~/.bashrc
echo "alias wormstop='pkill -f wormgpt && systemctl stop tor'" >> ~/.bashrc

echo -e "${GREEN}[+] Phase 9: Downloading Resources${NC}"
cd /opt/wormgpt 2>/dev/null || mkdir -p /opt/wormgpt && cd /opt/wormgpt
wget -q https://raw.githubusercontent.com/ultrafunkamsterdam/undetected-chromedriver/master/undetected_chromedriver/__init__.py 2>/dev/null || true
wget -q https://raw.githubusercontent.com/Anorov/cloudflare-scrape/master/cfscrape/__init__.py 2>/dev/null || true

echo -e "${GREEN}[+] Phase 10: Final Setup${NC}"
chmod +x /opt/wormgpt/wormgpt_main.py 2>/dev/null || true
chmod +x /usr/share/applications/wormgpt.desktop 2>/dev/null || true

echo ""
echo -e "${YELLOW}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║                    INSTALLATION COMPLETE!                ║${NC}"
echo -e "${YELLOW}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}[✅] Installation Successful!${NC}"
echo ""
echo -e "${YELLOW}[🚀] Usage Methods:${NC}"
echo "    1. Desktop: Search 'WORMGPT Nuclear' in applications"
echo "    2. Terminal: wormgpt"
echo "    3. With TOR: wormstart"
echo ""
echo -e "${YELLOW}[🎯] Quick Start:${NC}"
echo "    wormgpt https://target.com"
echo ""
echo -e "${RED}[⚠️] WARNING: For authorized testing only!${NC}"
echo -e "${RED}[💀] Illegal use may result in severe penalties!${NC}"
echo ""
echo -e "${GREEN}[🔄] Restart terminal or run: source ~/.bashrc${NC}"