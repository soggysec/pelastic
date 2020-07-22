
### Using the Pelastic tool

#### About
This tool has been forked and updated to import your Peloton workout stats into a local ELK stack. This has been tested on a Mac running
ELK inside of a Docker container.

#### Dependencies
```bash
pip install elasticsearch
```

This script requires you to install [Peloton-Client-Library](https://github.com/soggysec/peloton-client-library). You will also need to
update the ~/.config/pelastic.ini file with your specifics. See Docker Example below...

#### Configuration
Pelastic requires a configuration file, where the path (including file) is either pulled from the environment variable `PELASTIC_CONFIG`,
or looked for in the hard-coded `~/.config/pelastic.ini`

Example on Apple OS X.  Open the Terminal.app and enter the following
```bash
export PELASTIC_CONFIG=$HOME/pelastic.ini
```

Example Configuration File
```bash
[elastic]
local = yes
host = localhost
port = 9200
id = Your_Elastic_Cloud_ID
username = Your_Elastic_Cluster_Username
password = Your_Elastic_Cluster_Password
```

#### Docker Example
Download and install Docker on your machine, then get the ELK container by running:

```bash
sudo docker pull sebp/elk
```

If you're on MacOS there are a couple of requirements for running ELK inside of your image, those are documented
[here](https://elk-docker.readthedocs.io/#prerequisites), or you can just run

```bash
sudo docker run -e MAX_MAP_COUNT=262145 -p 5601:5601 -p 9200:9200 -p 5044:5044 -it --name elk sebp/elk
```

Now Elastic Search should be running on localhost:9200, which you can validate by using your browser.

Next you can run with the default configuration by running the following:

```bash
export PELASTIC_CONFIG=$PWD/pelastic.ini
python pelastic.py
```

If everything worked as expected, you should be able to browse to your data using Kibana by going to: http://localhost:5601
