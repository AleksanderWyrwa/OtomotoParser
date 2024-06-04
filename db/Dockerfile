# Use the official SQLite image as base
FROM alpine

# Install SQLite
RUN apk add --no-cache sqlite

# Copy the database file into the container
COPY cars.db /data/

# Set the working directory
WORKDIR /data

# Expose SQLite default port (if necessary for other services to access, usually not needed for SQLite)
EXPOSE 5432

# Run SQLite when the container launches
CMD ["sqlite3", "cars.db"]
