FROM mongo:latest

# Set root user
ENV MONGO_INITDB_ROOT_USERNAME root

# Define arg root_secret
ARG root_secret=defaultChangeM3!#

# Set env var with root password
ENV MONGO_INITDB_ROOT_PASSWORD ${root_secret}

# Set name of test database
ENV MONGO_INITDB_DATABASE test

# Add init script to init-db entry point
ADD ./js/init.js /docker-entrypoint-initdb.d/
# Add secrets to init-db entry point
ADD ./config/db_secrets /docker-entrypoint-initdb.d/
ADD ./config/root_secret /docker-entrypoint-initdb.d/

# Always start mongo in auth mode
ENTRYPOINT ["docker-entrypoint.sh", "--auth"]