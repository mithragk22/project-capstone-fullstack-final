#!/bin/bash
export DATABASE_URL="postgresql://postgres:hello@localhost:5432/postgres"
export EXCITED="true"
export DB_USER="postgres"
export DB_PASSWORD="hello"
export DB_NAME="mydb"
export AUTH0_DOMAIN="dev-eezq7zycigop1hot.us.auth0.com"
export API_AUDIENCE="castingAgency"
echo "setup.sh script executed successfully!"
