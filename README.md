
### Using the Pelastic tool

#### Download
https://github.com/codingogre/pelastic/archive/master.zip

#### Configuration
Pelastic requires a configuration file, where the path (including file) is either pulled from the environment variable `PELASTIC_CONFIG`,
or looked for in the hard-coded `~/.config/pelastic.ini`

Example on Apple OS X
```bash
export PELASTIC_CONFIG=$HOME/pelastic.ini
```

Example on Windows
```bash
[Environment]::SetEnvironmentVariable("PELASTIC", "C:\Users\wutan\pelastic.ini", "User")
```

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
Open the Terminal.app on Apple OS X and navigate to the folder where pelastic is downloaded

```bash
./pelastic.py
```

Open Powershell on Windows
```bash
python pelastic.py
```