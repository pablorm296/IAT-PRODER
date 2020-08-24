# Install nginx and python
apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -yq python-dev nginx python3-pip

# Install virtualenv
pip install virtualenv

# Set time zone
echo "America/Mexico_City" > /etc/timezone
ln -s -f /usr/share/zoneinfo/America/Mexico_City  /etc/localtime

dpkg-reconfigure --frontend noninteractive tzdata

# Restart apache
systemctl enable nginx
service nginx restart
