---
layout: default
---

Stedr lets you interact with it via the browser, native apps, command line and through a Rest API. 
This site will document usage of each of these tools, starting with the command line interface (CLI).

# Terminology
stedr == the location a camera (for the most part) or sensors are located
snap == A snapshot from a stedr, usually an image

In addition to being the name of the service, 'stedr' is the name of the location where we gather information. This is usually a camera that takes images, but could be an arbitrary set of sensors. A snap is a snapshot of the information gathered from one stedr (which again - is usaully an image, but could all sorts of things).

# CLI

The commmand line tool is called 'stedr' and helps you among other things to bulk upload and download images.

## Installation
Prerequisite is to have Python 3 installed (version >= 3.6.5). 

```bash
pip3 install -e 'git+https://github.com/smorgrav/stedr#egg=stedr&subdirectory=cli'
```

Requires python 3.6.5 or newer. If you don't have that or want to isolate the installation you can 
run it under a virtual environment. 

```bash
virtualenv -p python3.6 venv
. venv/bin/activate
````

If you need an introduction to pip and virtualenv, I found this one quite good: https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/

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
  cron
  dataflow
  snap
  stedr
  timelapse
```

For more help add '--help or -h' after the command you need more info about.

## Getting started
All commands agsint stedr needs authentication. This can be provided on the commandline for every command with the
apikey and uid parameters, but it will soon feel quite annoying to specify these each time. The alternative is to 
configure this once and for all, using the config command. The apikey, userid and endpoint are found under 'Settings' in the web UI. 
You might have to enable the API key and/or generate a new key as this is not provided by default. This is also done in the web UI.

```
$ stedr config set --uid myuid_usually_alooong_string --apikey even_longer_string --endpoint a_url_ofsomesort
```

## Help
To navigate the CLI you start by just typing 'stedr' and the help message under Usage will be printet. Any command and subcommand you choose have additional help instructions if you add '--help' at the end of the command. 

```
$ stedr snap download --help
Usage: stedr snap download [OPTIONS] SAVEDIR

Options:
  --stedr TEXT      The id of the stedr  [required]
  --imageid TEXT    The id of the image
  --imagelist FILE  A list of image ids
  --progress FILE   Progress file to support graceful retries for the list
  -h, --help        Show this message and exit.
```

## Example - download all images
If you want your images locally or need an additional backup, you can download all images from one stedr in a couple of steps. Let's pretend that we have a stedr called 'buvika'. Then the procedure would look like:

```
$ stedr snap list --stedr buvika --imagelist myimages 
$ stedr snap download --stedr buvika --imagelist myimages mydirectory
```

The first command would download all ids in a file called myimages. The imagelist option is optional and you could use the console output instead if you prefeered thast. 

The second command points to the image list file we generated with the first command and starts downloading. If you have a lot of files then you could add the --progress option to support graceful retryes (avoid downloading same image twice when you restart the command).

The files will be saved in a hiararchy under the mydirectory directory. 

## Example - upload images
You might have a bunch of older images that you would like to upload to stedr. 

TBD

# Setting up a web camera

## By email

## By url

# REST API
The best documentation so far is to look at the stedr source at https://github.com/smorgrav/stedr and derive it from there. 
