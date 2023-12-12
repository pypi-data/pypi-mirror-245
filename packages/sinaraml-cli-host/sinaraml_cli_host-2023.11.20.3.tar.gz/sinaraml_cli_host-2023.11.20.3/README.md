# Description
This the SinaraML CLI library plugin. It enables you to use server and model CLI commands. Needs sinara_cli package to work

# CLI Installation
Linux / WSL:
```
sudo pip install sinaraml_cli_host
```

Windows:
```
pip install sinaraml_cli_host
```

# CLI Quick Start
Commands start with the keyword sinara (similar to git, docker, kubectl)<br>
If a command call is made without a mandatory parameter, help is displayed on the available parameters and methods of calling the command, for example:

```
~$ sinara
usage: sinara [-h] {server,model} ...

options:
  -h, --help            show this help message and exit

subject:
  {server,model,pipeline}
                        subject to use [server, model, pipeline]
    server              server subject
    model               model subject
    pipeline            pipeline subject
```

```
~$ sinara server
usage: sinara server [-h] {create,start} ...

options:
  -h, --help      show this help message and exit

action:
  {create,start}  Action to do with subject [create, start, stop, etc]
    create        create action
    start         start action
```