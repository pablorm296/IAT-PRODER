# Copy repo
git clone https://github.com/pablorm296/IAT-PRODER.git /srv/IAT

# Make a virtual env
pip3 install virtualenv
virtualenv /srv/IAT/Env

# Install requirements
 /bin/bash -c "source /srv/IAT/Env/bin/activate && pip install -r /srv/IAT/requirements.txt && pip install -e /srv/IAT/Src"
