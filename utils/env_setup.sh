#!/bin/bash

# IMPORTANT: If running this script fails with a syntax error then open this file in vim and issue ":set ff=unix" to fix it
# and save the file using ":wq". This error is because of LineEndings mismatch, reset it to unix endings using above command.

#######################################################################################
# Summary
# -------
# This script will setup PostgreSQL, Pipenv and some core tools required to stage a dev-like environment for DSIM's own applications and services.
# Currently only an upstart/systemd based init systems are supported.
# Running this script on pseudo-linux systems isn't allowed and is explicitly discouraged.
# This script is really only meant to be used on Crabuntu LTS versions only (supported between >= 14.04 and <= 18.04)
# Note: Support for Focal Fossa (20.04) maybe added if all the APT repos for Postgres and co are updated in-time.
#
# Overview of actions performed:
#	1. Updates and Upgrades all installed packages on system using `apt` command.
#	2. Remove any existing installations of PostgreSQL, Pipenv and other dependent tools.
#	3. Performs a fresh install of PGSQL latest-available version, tools like pg-admin, pg-tune and co.
#   4. Optionally setup the DB schema (useless as backend abstracts it via ORM) but useful nevertheless to get an inital state of DB
#
# Created on 10-May-2020, 10:30 (UTC +5:30) (git blame //apoolla)
# Last Updated on 6-Aug-2020 10:15 (UTC +5:30)
#######################################################################################
# message colors.
info_text_blue=$(tput setaf 7);
normal_text=$(tput sgr0);
error_text=$(tput setaf 1);
status_text_yellow=$(tput setaf 3);

msg(){
    printf "\n${status_text_yellow}$1${normal_text}\n\n"
}

error(){
    printf "\n${error_text}Error: $1${normal_text}\n"
}

info(){
    printf "\n${info_text_blue}$1${normal_text}\n"
}
function setup_uwsgi() {
    msg "Setting up uwsgi server..."
    sudo apt-get install libpcre3 libpcre3-dev libssl-dev; \
    sudo CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" UWSGI_PROFILE_OVERRIDE=ssl=true; \
    msg "uwsgi setup completed successfully" || error "Failed to setup uwsgi server."
}
function main() {
   setup_uwsgi
}

main
