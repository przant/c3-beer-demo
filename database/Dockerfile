FROM postgres:16-bookworm

# Copy initialization script
# PostgreSQL automatically runs any .sql files in /docker-entrypoint-initdb.d/ on first startup
COPY init.sql /docker-entrypoint-initdb.d/

# The dataset CSV will be mounted as a volume, so PostgreSQL can access it
# See docker-compose.yml for volume configuration
