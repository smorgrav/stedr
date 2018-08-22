---
layout: default
---

Stedr lets you interact with it via web, app, command line and through a Rest API. 

# CLI

The commmand line tool is called 'stedr' and helps you among other things bulk upload and download images.


```bash
pip install -e 'git+git@github.com:smorgrav/stedr.git#egg=stedr&subdirectory=cli'
```

## Usage
```
Usage: stedr [OPTIONS] COMMAND [ARGS]...

  The command line for Stedr - know your place!

Options:
  -v, --verbose        Print out more for each command
  -n, --dryrun         Do as much as possible without changing anything
  -e, --endpoint TEXT  Override configured endpoint
  -k, --apikey TEXT    Override configured apikey
  -u, --uid TEXT       Override configured uid
  -h, --help           Show this message and exit.

Commands:
  config
  upload
```

For more help add '--help' after the command and subcommands you need more info about.

# Documentation

## Setting up a web camera

## Bulk upload images


# REST API

## Authorization
* Enable apikey
* Be owner of the stedr you want to operate on

## Snap
/api/snap/{stedr}

Describe request


