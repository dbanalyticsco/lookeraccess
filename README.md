# lookeraccess

## Installation 

*N.B.*: Once setuptools is implemented, installation should be done via `pip`.

To 'install' `lookeraccess`, you need clone the repo and install the required packages. It is best to use a virtual environment to install the packages.

```shell
git clone git@github.com:dbanalyticsco/lookeraccess.git
cd lookeraccess
virtualenv venv
pip install -r requirements.txt
```

## Setup

In order to run, `lookeraccess` will look for three environment variables: `LOOKER_BASE_URL`, `LOOKER_CLIENT_ID`, `LOOKER_CLIENT_SECRET`. You will need to set them up before running the package. 

The `LOOKER_BASE_URL` is simply the URL of your Looker instance.

The `LOOKER_CLIENT_ID` and `LOOKER_CLIENT_SECRET` are the API credentials of the user as whom you would like to run the package. You need to ensure that the ensure has the correct permissions to make all the changes you make. Ideally, this would be an Admin user. You can find more information on getting the API credentials [in the Looker documentation]().

## Running lookeraccess

Until we implement setuptools for the project, the project will get run as a python script through the entrypoint `lookeraccess/runner.py`.

### Check your connection

To check if your credentials are setup correctly, run the `connect` command. From the projects root folder, run:

```shell
python lookeraccess/runner.py connect
```