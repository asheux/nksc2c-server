#!/bin/bash

# docker-compose run -p 8000:8000 app "$@"
docker compose -f docker-compose.dev.yml run -p 8000:8000 app "$@"
