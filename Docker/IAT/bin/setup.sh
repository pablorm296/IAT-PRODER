# Install nginx and python
apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -yq nginx systemd python3.6 which

# Set time zone
echo "America/Mexico_City" > /etc/timezone
ln -s -f /usr/share/zoneinfo/America/Mexico_City  /etc/localtime

dpkg-reconfigure --frontend noninteractive tzdata

# Restart nginx
systemctl enable nginx
service nginx restart
