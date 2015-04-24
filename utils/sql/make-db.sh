#!/bin/bash

printf "\nCREATING DATABASE...\n"

gosu postgres postgres --single <<- EOSQL
    CREATE USER docker;
    CREATE DATABASE edx_courseware;
    GRANT ALL PRIVILEGES ON DATABASE edx_courseware TO docker;
EOSQL

printf "\nFINISHED CREATING DATABASE...\n"
