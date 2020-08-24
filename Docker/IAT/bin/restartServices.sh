# Restart nginx
service nginx restart

# Copy repo
git clone git@github.com:pablorm296/IAT-PRODER.git /srv/IAT

# Make a virtual env
virtualenv /srv/IAT/env

# Install requirements
source /srv/IAT/env/bin/activate

pip install -r /srv/IAT/requirements.txt
