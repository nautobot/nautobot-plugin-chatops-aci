# Nautobot Cisco ACI Chatops Plugin

The [Nautobot](https://github.com/nautobot/nautobot) Cisco ACI Chatops Plugin extends the [Nautobot Chatops](https://github.com/nautobot/nautobot-plugin-chatops/) framework to interact with a Cisco APIC (Application Policy Infrastructure Controller) using commands in Slack, Webex, Microsoft Teams, and Mattermost.  
 
## Screenshots
  
![image](https://user-images.githubusercontent.com/6945229/139871492-6a557f30-65d2-4015-a8f9-c8b9f5f22f88.png)

![image](https://user-images.githubusercontent.com/6945229/139872921-93f14a1d-68c0-4295-a5b3-dcc685c97a5a.png)

![image](https://user-images.githubusercontent.com/6945229/139872116-5a99004a-364b-4a3b-b927-6ca64522ef09.png)
  

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

```shell
pip install nautobot-plugin-chatops-aci
```

Once installed, the plugin needs to be enabled in your `nautobot_config.py`

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_chatops", "nautobot_plugin_chatops_aci"]
```

In addition,  add the below `PLUGINS_CONFIG` section to `nautobot_config.py`.   

```python
# Also in nautobot_config.py
PLUGINS_CONFIG = {
    "nautobot_chatops": {
        "enable_slack": os.environ.get("ENABLE_SLACK"),
        "enable_ms_teams": os.environ.get("ENABLE_MS_TEAMS"),
        "enable_webex": os.environ.get("ENABLE_WEBEX"),
        "microsoft_app_id": os.environ.get("MICROSOFT_APP_ID"),
        "microsoft_app_password": os.environ.get("MICROSOFT_APP_PASSWORD"),
        "slack_api_token": os.environ.get("SLACK_API_TOKEN"),
        "slack_signing_secret": os.environ.get("SLACK_SIGNING_SECRET"),
        "slack_slash_command_prefix": os.environ.get("SLACK_SLASH_COMMAND_PREFIX", "/"),
        "webex_token": os.environ.get("WEBEX_TOKEN"),
        "webex_signing_secret": os.environ.get("WEBEX_SIGNING_SECRET"),
        "enable_mattermost": False,
        "mattermost_api_token": os.environ.get("MATTERMOST_API_TOKEN"),
        "mattermost_url": os.environ.get("MATTERMOST_URL"),
    },
    "nautobot_chatops_aci": {"aci_creds": {x: os.environ[x] for x in os.environ if "APIC" in x}},
}
```
The `aci_creds` setting above creates a Python dictionary which imports any environment variables prefixed with `APIC`. The following environment variables are needed to define each APIC hostname and credentials:

```python
APIC_USERNAME_NTCAPIC={{ APIC username }}
APIC_PASSWORD_NTCAPIC={{ APIC password }}
APIC_URI_NTCAPIC={{ https://apic_hostname }}
APIC_VERIFY_NTCAPIC={{ Check SSL certificate (True or False) }}
```
The text `NTCAPIC` in the above variable names can be replaced with an identifier of your choosing.  It will show up in the APIC selection dialogue when executing commands as shown below.  
  
![image](https://user-images.githubusercontent.com/6945229/139917084-c30a2b8b-940a-4e23-bca4-2ab7bf7f6ed0.png)
  
With this syntax, it is possible to support multiple APICs. For example, to add another APIC to the selection list we could specify a second set of credentials:

```python
APIC_USERNAME_DEVNET={{ APIC username }}
APIC_PASSWORD_DEVNET={{ APIC password }}
APIC_URI_DEVNET={{ https://apic_hostname }}
APIC_VERIFY_DEVNET={{ Check SSL certificate (True or False) }}
```
When executing chat commands, we would then be presented with a selection dialog containing both `ntcapic` and `devnet`.  

In addition, the following environment variables are required for the chat platform in use:

```python
# Slack
ENABLE_SLACK=true
SLACK_API_TOKEN=foobar
SLACK_SIGNING_SECRET=foobar

# Webex
ENABLE_WEBEX=true
WEBEX_TOKEN=foobar
WEBEX_SIGNING_SECRET=foobar

# Mattermost
ENABLE_MATTERMOST=false
MATTERMOST_API_TOKEN=foobar
MATTERMOST_URL=foobar

ENABLE_MS_TEAMS=false
MICROSOFT_APP_ID=foobar
MICROSOFT_APP_PASSWORD=foobar
```

> When deploying as Docker containers, the above environment variables should be defined in the file `development/creds.env`. An example credentials file `creds.env.example` is available in the `development` folder.  


## Usage
### Command Setup
Add a top level command named `aci` to the platform you are using. See the [Platform-specific Setup](https://github.com/nautobot/nautobot-plugin-chatops/blob/develop/docs/chat_setup/chat_setup.md#platform-specific-setup) section of the [Nautobot Chatops Installation Guide](https://github.com/nautobot/nautobot-plugin-chatops/blob/develop/docs/chat_setup/chat_setup.md) for instructions specific to Slack, Microsoft Teams, WebEx, and Mattermost.  

The following commands are available:

| Command | Description |
| ------- | ----------- |
| get-tenants [apic] | Display tenants configured in Cisco ACI.|
| get-aps [apic] [tenant] | Display Application Profiles configured in Cisco ACI.|
| get-epgs [apic] [tenant] [ap] | Display Endpoint Groups (EPGs) configured in Cisco ACI.|
| get-epg-details [apic] [tenant] [ap] [epg] | Display details for an Endpoint Group in Cisco ACI.|
| get-vrfs [apic] [tenant] | Display vrfs configured in Cisco ACI.|
| get-bds [apic] [tenant] | Display Bridge Domains configured in Cisco ACI.|
| get-pending-nodes [apic] |  Display unregistered nodes in Cisco ACI.|
| get-nodes [apic] | Display fabric nodes in Cisco ACI.|
| get-controllers [apic] | Display APIC controllers in Cisco ACI.|
| get-interfaces [apic] [pod-id] [node-id] [state] | Display interfaces on a specified node in Cisco ACI.|
| register-node [apic] [serial-nbr] [node-id] [name] | Register a new fabric node in Cisco ACI.|
|  

## Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:

- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.

### Development Environment

The development environment can be used in 2 ways. First, with a local poetry environment if you wish to develop outside of Docker. Second, inside of a docker container.

#### Invoke tasks

The [PyInvoke](http://www.pyinvoke.org/) library is used to provide some helper commands based on the environment.  There are a few configuration parameters which can be passed to PyInvoke to override the default configuration:

* `nautobot_ver`: the version of Nautobot to use as a base for any built docker containers (default: latest)
* `project_name`: the default docker compose project name (default: nautobot-plugin-chatops-aci)
* `python_ver`: the version of Python to use as a base for any built docker containers (default: 3.6)
* `local`: a boolean flag indicating if invoke tasks should be run on the host or inside the docker containers (default: False, commands will be run in docker containers)
* `compose_dir`: the full path to a directory containing the project compose files
* `compose_files`: a list of compose files applied in order (see [Multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files) for more information)

Using PyInvoke these configuration options can be overridden using [several methods](http://docs.pyinvoke.org/en/stable/concepts/configuration.html).  Perhaps the simplest is simply setting an environment variable `INVOKE_NAUTOBOT-PLUGIN-CHATOPS-ACI_VARIABLE_NAME` where `VARIABLE_NAME` is the variable you are trying to override.  The only exception is `compose_files`, because it is a list it must be overridden in a yaml file.  There is an example `invoke.yml` in this directory which can be used as a starting point.

#### Local Poetry Development Environment

1.  Copy `development/creds.env.example` to `development/creds.env` (This file will be ignored by git and docker)
2.  Uncomment the `POSTGRES_HOST`, `REDIS_HOST`, and `NAUTOBOT_ROOT` variables in `development/creds.env`
3.  Create an invoke.yml with the following contents at the root of the repo:

```shell
---
nautobot_plugin_chatops_aci:
  local: true
  compose_files:
    - "docker-compose.requirements.yml"
```

3.  Run the following commands:

```shell
poetry shell
poetry install
export $(cat development/dev.env | xargs)
export $(cat development/creds.env | xargs) 
```

4.  You can now run nautobot-server commands as you would from the [Nautobot documentation](https://nautobot.readthedocs.io/en/latest/) for example to start the development server:

```shell
nautobot-server runserver 0.0.0.0:8080 --insecure
```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

#### Docker Development Environment

This project is managed by [Python Poetry](https://python-poetry.org/) and has a few requirements to setup your development environment:

1.  Install Poetry, see the [Poetry Documentation](https://python-poetry.org/docs/#installation) for your operating system.
2.  Install Docker, see the [Docker documentation](https://docs.docker.com/get-docker/) for your operating system.

Once you have Poetry and Docker installed you can run the following commands to install all other development dependencies in an isolated python virtual environment:

```shell
poetry shell
poetry install
invoke start
```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

### CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`. 

Each command can be executed with `invoke <command>`. Environment variables `INVOKE_NAUTOBOT-PLUGIN-CHATOPS-ACI_PYTHON_VER` and `INVOKE_NAUTOBOT-PLUGIN-CHATOPS-ACI_NAUTOBOT_VER` may be specified to override the default versions. Each command also has its own help `invoke <command> --help`

#### Docker dev environment

```no-highlight
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  restart          Restart Nautobot and its dependencies.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
```

#### Utility

```no-highlight
  cli              Launch a bash shell inside the running Nautobot container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  nbshell          Launch a nbshell session.
```

#### Testing

```no-highlight
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  flake8           This will run flake8 for the specified name and Python version.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  pylint           Run pylint code analysis.
  tests            Run all tests for this plugin.
  unittest         Run Django unit tests for the plugin.
```

## Questions

For any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).
Sign up [here](http://slack.networktocode.com/)


