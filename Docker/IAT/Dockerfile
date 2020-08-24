FROM ubuntu:latest

# Set time zone
ENV TZ=America/Mexico_City

# Makee sure we are in /root/
WORKDIR /root/

# Copy bin dir
COPY bin .

# Copy config dir
COPY config .

# Run setup script
RUN ./setup.sh

# Copy nginx config file
RUN ["cp", "./nginx.conf", "/etc/nginx/nginx.conf"]

# Create server directories
RUN ["mkdir", "-p", "/srv/IAT/"]

# Run restart script
RUN ./restartServices.sh

# Expose port 80 (Nginx)
EXPOSE 80

# Define environment variables
ENV FLASK_DEBUG_IAT="True"
ENV VIRTUAL_ENV /srv/IAT/Env
ENV PATH /srv/IAT/Env/bin:$PATH

RUN which python 

CMD ["python", "/srv/IAT/Src/IAT/server.py"]
