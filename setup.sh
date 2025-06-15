#!/bin/bash
export DATABASE_URL="postgresql://postgres:hello@localhost:5432/postgres"
export EXCITED="true"
export DB_USER="postgres"
export DB_PASSWORD="hello"
export DB_NAME="mydb"
echo "setup.sh script executed successfully!"