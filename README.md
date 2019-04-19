# lookeraccess

## Installation 

To install `lookeraccess`, you need clone the repo and install the required packages. It is best to use a virtual environment to install the packages.

```shell
git clone git@github.com:dbanalyticsco/lookeraccess.git
cd lookeraccess
virtualenv venv
source venv/bin/activate
pip install -e .
```

## Setup

In order to run, `lookeraccess` will look for three environment variables: `LOOKER_BASE_URL`, `LOOKER_CLIENT_ID`, `LOOKER_CLIENT_SECRET`. You will need to set them up before running the package. 

The `LOOKER_BASE_URL` is simply the URL of your Looker instance.

The `LOOKER_CLIENT_ID` and `LOOKER_CLIENT_SECRET` are the API credentials of the user as whom you would like to run the package. You need to ensure that the ensure has the correct permissions to make all the changes you make. Ideally, this would be an Admin user. You can find more information on getting the API credentials [in the Looker documentation](https://docs.looker.com/admin-options/settings/users).

## Running lookeraccess

### Command: connect

To check if your credentials are setup correctly, run the `connect` command. From the projects root folder, run:

```shell
lookeraccess connect
```

### Command: pull

To pull your current Looker configuration, run the `pull` command. It will generate four files in your repo: `permission_sets.yml`, `model_sets.yml`, `roles.yml` and `groups.yml`. These should reflect your Looker configuration at that point in time. 

The standard, non-editable objects will not be present in your files. i.e. The permission set 'Admin', the model set 'All' and the group 'All Users' will be missing.

```shell
lookeraccess pull
```

### Command: validate

After you make changes to your config files that you pulled above, you can validate the schema and changes with the `validate` command. This will ensure that your files are in the correct format and that all the references are valid. i.e. you aren't referencing a permission or model that doesn't exit. 

If the command runs without raising an Exception, your files are good:

```shell
lookeraccess validate
```

### Command: changes

To see the changes that `lookeraccess` will implement, run the `changes` command. It will pull the current config (`pull`) and identiy all the groups, roles, model sets and permission sets that needs to be either created, deleted or updated.

```shell
lookeraccess changes
```

### Command: run

To push changes back to Looker, use the `run` command. It will effectively run `connect`, `pull`, `validate` before pushing the changes to Looker.

```shell
lookeraccess run
```

## Options

### --port

`lookeraccess` defaults to assume you use the port 19999. If that is not the case, use the `--port` option to set the port you would like to use.

```shell
lookeraccess changes --port 432
```

### --uselog



