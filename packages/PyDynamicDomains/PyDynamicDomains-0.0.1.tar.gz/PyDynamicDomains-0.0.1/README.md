# PyDynamicDomains - A Dynamic Domain Name System Record Updater for Google Domains

## Description

This package is designed for use with Google Domains dynamic DNS records.  
The intent is for this package to be installed on a server whose public IP address is dynamically allocated.
Once installed, it may be run via Cron/Crontab to check for public IP changes and update associated DDNS records appropriately.

## Limitations

Only supports *Nix systems associated with Google Domains (https://domains.google.com).

## Setup

Edit the `dynamic-dns.ini` file located at `/home/%username%/.local/share/pydynamicdomains/`.
The package will create an example file for you at this %PATH% on first run.

