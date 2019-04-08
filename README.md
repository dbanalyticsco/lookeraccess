# lookeraccess

## Installation 

*N.B.*: Once setuptools is implemented, installation should be done via `pip`.

To 'install' `lookeraccess`, you need clone the repo and install the required packages. It is best to use a virtual environment to install the packages.

```shell
git clone git@github.com:dbanalyticsco/lookeraccess.git
cd lookeraccess
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Setup

In order to run, `lookeraccess` will look for three environment variables: `LOOKER_BASE_URL`, `LOOKER_CLIENT_ID`, `LOOKER_CLIENT_SECRET`. You will need to set them up before running the package. 

The `LOOKER_BASE_URL` is simply the URL of your Looker instance.

The `LOOKER_CLIENT_ID` and `LOOKER_CLIENT_SECRET` are the API credentials of the user as whom you would like to run the package. You need to ensure that the ensure has the correct permissions to make all the changes you make. Ideally, this would be an Admin user. You can find more information on getting the API credentials [in the Looker documentation](https://docs.looker.com/admin-options/settings/users).

## Running lookeraccess

*N.B.*: Until we implement setuptools for the project, the project will get run as a python script through the entrypoint `lookeraccess/runner.py`.

### Command: connect

To check if your credentials are setup correctly, run the `connect` command. From the projects root folder, run:

```shell
python lookeraccess/runner.py connect
```

### Command: pull

To pull your current Looker configuration, run the `pull` command. It will generate four files in your repo: `permission_sets.yml`, `model_sets.yml`, `roles.yml` and `groups.yml`. These should reflect your Looker configuration at that point in time. 

The standard, non-editable objects will not be present in your files. i.e. The permission set 'Admin', the model set 'All' and the group 'All Users' will be missing.

```shell
python lookeraccess/runner.py pull
```

### Command: validate

After you make changes to your config files that you pulled above, you can validate the schema and changes with the `validate` command. This will ensure that your files are in the correct format and that all the references are valid. i.e. you aren't referencing a permission or model that doesn't exit. 

If the command runs without raising an Exception, your files are good:

```shell
python lookeraccess/runner.py validate
```

### Command: changes

TODO: implement changes command to verify changes that will occur from `run` command.

### Command: run

TODO: implement run command that push your file config to your Looker instance.