#!/bin/bash
# RUN like `source eport_locals.sh` 

# Load environment variables from .env file
if [ -f ./.env ]; then
  echo "Loading environment variables from ./.env"
  export $(grep -v '^#' ./.env | xargs)
else
  echo ".env file not found at ./.env!"
  exit 1
fi

# Optional: Print loaded variables (for debugging purposes)
echo "Environment variables loaded successfully."

