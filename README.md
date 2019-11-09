# BJCP-ELK Basic analytics on the Beer Judge Certification Program Style Guide

BJCP is the [Beer Judge Certification Program](https://bjcp.org/), that among other things produces a beer style guidelines.

> The BJCP grants the right to make copies of the Style Guide for use in
> BJCP-sanctioned competitions or for educational/judge training purposes.
> All other rights reserved.

This repository uses the content of the 2015 BJCP Style Guide only as an educational/training and personal purposes.

The original 2015 BJCP Style Guide reference can be found on https://www.bjcp.org/.

ELK is a stack composed of [Elasticsearch](https://www.elastic.co/products/elastic-stack) and [Kibana](https://www.elastic.co/products/kibana) that provides at-a-glance insights into the Style Guide and enables you to drill down into details.

## Screenshots

The default dashboard with 124 Sub categories of beer:
![BJCP Analytics](./bjcp-analytics.png)

Filtering on the Stout family:
![BJCP Analytics](./bjcp-analytics-filter.png)

Searching for a beer with citrus aroma and low bitterness:
![BJCP Analytics](./bjcp-analytics-search.png)

## Installation

### Requirements

You need to install: 
- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

For Mac OS, you have to update your `/etc/hosts` and add the following lines:
```bash
127.0.0.1 elastic.docker.localhost
127.0.0.1 kibana.docker.localhost
```

### Start the EK Stack

Open a terminal and run:
```bash
docker-compose up
```

The first time it will take time to download docker images, have a beer.
The stack is up when you see some output like:

```bash
elastic          | {"type": "server", "timestamp": "2019-11-08T09:06:08,264Z", "level": "INFO", "component": "o.e.c.r.a.AllocationService", "cluster.name": "docker-cluster", "node.name": "elastic", "message": "Cluster health status changed from [YELLOW] to [GREEN] (reason: [shards started [[.kibana_1][0]]]).", "cluster.uuid": "76sBrZV1SXuR6CyjlGsFZQ", "node.id": "DK5p_IskRhuPpoWUmfm9Qg"  }
...
kibana           | {"type":"log","@timestamp":"2019-11-08T09:06:08Z","tags":["info","http","server","Kibana"],"pid":7,"message":"http server running at http://0:5601"
```

### Load the Style Guide into Elasticsearch

When the stack is started, run the `load.sh` script: 

```bash
./load.sh
```

### Initialize the Kibana dashboard

1. Open a browser on: http://kibana.docker.localhost/app/kibana#/management/kibana/index_patterns
  
   - Click on `Create an index pattern`
   - Enter index pattern: `bjcp*`
   - Then `> Next Step` and `> Create index pattern`
    
2. Now import the dashboard from the management saved object tab:
   http://kibana.docker.localhost/app/kibana#/management/kibana/objects
   
   - Click on `Import`
   - Then select the `./export.ndjson` file and `Import`
   - Change the index to `bjcp*`
   - Click on `Confirm All changes`

3. Go to the dashboard page and open the `bjcp` dashboard:
   http://kibana.docker.localhost/app/kibana#/dashboards

      
## Usage

Once the installation is done, the stack can be stop:
```bash
docker-compose down --volume
```

And restart:
```bash
docker-compose up -d
```

The Dashboard is persisted on the `./data` directory so you can customize the dashboard.

## Dev

### About the data

The 2015 BJCP Style Guide has been turned into a JSON version and augmented with few metadata:

- `origin`: as described in [Styles Sorted Using Country of Origin](https://dev.bjcp.org/beer-styles/4-styles-sorted-using-country-of-origin/)
- `family`: as described in [Styles Sorted Using Style Family](https://dev.bjcp.org/beer-styles/3-styles-sorted-using-style-family/)
- `family_history`: as described in [Styles Sorted Using History](https://dev.bjcp.org/beer-styles/5-styles-sorted-using-history/) 

The original and terminal extract are in Plato instead of SG. 

For now only the subcategories are injected into Elasticsearch, some fields are added:

- vital statistics averages: `alcohol.avg`, `original_extract.avg`, `terminal_extract.avg`, `bitterness.avg`, `color.avg`
- subcategory names are prefixed with id formatted in sortable way (i.e 1A is rewrittend as 01A) 

 
### Extract data from JSON to Elasticsearch bulk format

Run the python script to generate the `bjcp-es.json` file: 
```bash    
./extract.py > ./bjcp-es.json
```
