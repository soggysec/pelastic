

As I've been poking around in your WebUI, I've essentially been looking at the API calls that are made. I've
been keeping notes on all of this [here](https://github.com/geudrik/peloton-api/blob/master/API_DOCS.md).

### Using the Pelastic tool

#### Configuration
Pelastic requires a configuration file, where the path is either pulled from the environment variable `PELASTIC_CONFIG`,
or looked for in the hard-coded `~/.config/pelastic.ini`

```bash
[peloton]
username = Your_Peloton_Username_Or_Email
password = Your_Peloton_Password

[elastic]
id = Your_Elastic_Cloud_ID
username = Your_Elastic_Cloud_Username
password = Your_Elastic_Cloud_Password
```

#### Example Usage
```bash
pelastic.py