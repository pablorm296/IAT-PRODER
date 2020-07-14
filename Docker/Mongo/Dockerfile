FROM mongo:latest

# Set global variables (root user and root password)
ENV MONGO_INITDB_ROOT_USERNAME root
ENV MONGO_INITDB_ROOT_PASSWORD wMvHrycPA5kTE9Px8YzE
# Init a test database
ENV MONGO_INITDB_DATABASE test

# Add init script to init-db entry point
ADD ./js/init.js /docker-entrypoint-initdb.d/

# Always start mongo in auth mode
ENTRYPOINT ["docker-entrypoint.sh", "--auth"]