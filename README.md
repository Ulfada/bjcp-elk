# BJCP-ELK Basic analytics on the Beer Judge Certification Program Style Guide

"The BJCP grants the right to make copies of the Style Guide for use in
BJCP-sanctioned competitions or for educational/judge training purposes.
All other rights reserved."

This tools should be seen as a educational/training purpose, the only Style Guide reference 
is on https://www.bjcp.org/.

EK is a stack composed of [Elasticsearch](https://www.elastic.co/products/elastic-stack) and [Kibana](https://www.elastic.co/products/kibana) that provides a way to intropect the Beer Style Guide.

## Requirements

You need to install: 
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Start the EK Stack

Open a terminal and run:
```bash
docker-compose up
```

## Load the Style Guide into Elasticsearch

```bash
./load.sh
```

## Initialize the Kibana dashboard

For Mac OS user update your `/etc/hosts` and add the following lines:
```bash
127.0.0.1 elastic.docker.localhost
127.0.0.1 kibana.docker.localhost
```

1. Open a browser on:  http://kibana.docker.localhost

2. Go to the Management tab > Index Patterns > Create an index pattern > index pattern: "bjcp" > Next Step > Create Index pattern

3. Go to the Management tab > Saved Objects > Import the file `./export.json` > Open > Import
   change the index to "bjcp" if necessary > Confirm All changes

4. Go to the dashboard > bjcp > Enjoy


## Dev

### Extract the Styles Guide from JSON to Elasticsearch bulk format

Generate the bjcp-es.json file from the bjcp-2015.json file: 
```bash    
./extract.py > ./bjcp-es.json
```
