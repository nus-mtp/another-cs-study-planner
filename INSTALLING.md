# Project Installation

This document details how you should set up the project.

## Contents

* Setup
  * [With Vagrant](#with-vagrant)
  * [Without Vagrant](#without-vagrant)
* Configuring The Database Settings
  * [Editing `/vagrant_setup/bootstrap.sh` (for Vagrant Users)](#editing-vagrant_setupbootstrapsh-for-vagrant-users)
  * [Editing `/components/local_database_data.py` (for both Vagrant and non-Vagrant users)](#editing-componentslocal_database_datapy-for-both-vagrant-and-non-vagrant-users)
* [Project Files & Structures](#project-files--structure)
* [Building and Running in Development Mode](#building-and-running-in-development-mode)
* [Building and Running in Production Mode](#building-and-running-in-production-mode)
* [Commonly Faced Issues](#commonly-faced-issues)
* [Other Issues](#other-issues)

## Setup

### With Vagrant

#### Prerequisites

You will require the following software to be installed on your machine, before you can perform project setup with Vagrant:

* [Vagrant](https://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (currently using version 5.1.18)

To setup the development environment, do the following:

1. Modify the following files accordingly to match your desired PostgreSQL settings:
    * `bootstrap.sh` in `/vagrant_setup`
    * `local_database_data.py` in `/components`
    * Click [here](#configuring-the-database-settings) to see how you should modify these files.
2. Run the command `vagrant up` in your console/terminal to set-up the virtual environment.
3. Run `vagrant ssh` to enter the environment and do `cd csmodify` to access the project files in the environment.

### Without Vagrant

#### Prerequisites

You will require the following software to be installed on your machine, before you can perform project setup without Vagrant:

##### Core platform/plugins
* [Python 2.7](https://www.python.org/downloads/) (currently using version 2.7.12)
* [web.py](http://webpy.org/install)
* [PostgreSQL](https://www.postgresql.org/download/)
* [psycopg2](https://pypi.python.org/pypi/psycopg2)
* [nose](https://pypi.python.org/pypi/nose/1.3.7)
* [paste](https://pypi.python.org/pypi/Paste)

##### Supplementary plugins
* [pylint](https://www.pylint.org/#install)

Lastly, you will need to configure `local_database_data.py`. Instructions can be found [here](#configuring-the-database-settings).

## Configuring The Database Settings

Our default database settings assumes that you are using the `postgres` database as the `postgres` user with password '12345678', using the `localhost` connection at port `5432`.

Based on our understanding, the default database user is `postgres` and the default database is `postgres`, with no password required, with the database accessible with `localhost` on port `5432`. Therefore, we expect that you will only need to change the password settings for the database.

Should your settings differ from ours, please read this section carefully.

### Editing `/vagrant_setup/bootstrap.sh` (for Vagrant Users)

* If you are using a different database user, you need to add commands in this file, that will:
  * Create a new user in PostgreSQL
  * Login to PostgreSQL with this user
* If `postgres` database does not exist in your database, you need to add a command in this file, that will create the `postgres` database for you.
* If you are using a different password to login to your PostgreSQL, simply change the variable `DB_PASSWORD` in the file.
* If you do not need a password to login to your PostgreSQL, you only need to remove the `ALTER USER` command that is present in the file.

### Editing `/components/local_database_data.py` (for both Vagrant and non-Vagrant users)

* Simply modify these variables in the file to match your database settings:
  * `database_name`
  * `user_name`
  * `password`
  * `host_name`
  * `port`
* **For Vagrant users:** make sure that these settings tally with your modifications to `/vagrant_setup/bootstrap.sh`

## Project Files & Structure

1. `app.py`
  * The Python script for running the application
  * To run the application locally, simply invoke this script using the command `python app.py`

2. `/components`
  * Contains all logical components for the application
  * This folder contains:
    * `/handlers` (containing Python scripts acting as handlers for web requests)
    * `database_adapter.py` (handles connection to database and database repopulation)
    * `local_database_data.py` (stores data and getters for local database connection)
    * `model.py` (acts as a facade for important logical components the database, such as `database.py`, `helper.py` and `check_string.py`)

3. `/static`
  * This resource folder is split into:
    * `/fonts` (for font resource files)
    * `/stylesheets` (for CSS stylesheets)
    * `/javascripts` (for JS scripts)
    * `/images` (for image resource files)

4. `/templates`
  * Contains all the web.py HTML template files to be rendered by the application

5. `/test`
  * Contains all test scripts

6. `/utils`
  * Contains internal scripts required by the application.

7. `.travis.yml`
  * Used for building the app environment in Travis CI

8. `Procfile`
  * Defines how Heroku should run the application when it is deployed.

9. `requirements.txt`
  * Defines the Python dependencies required by the application, when it is deployed on Heroku.

10. `dbclean.py`
  * A Python script used to rebuild the aplication's database during development stage, when needed.
  * You can run this script using the command `python dbclean.py`

## Building and Running in Development Mode

Simply set `web.config.debug` to `True` in `app.py`, which will allow the stack trace to be displayed upon the app's failure. Once this is done, you can view your app by running `python app.py` and accessing it on `localhost:8080`.

## Building and Running in Production Mode

Simply set `web.config.debug` to `False`, and you are ready to push your app out for production. You can then choose to deploy this app to the deployment platform that you desire.

To access the app, you can just access the URL where your app is deployed to.

## Commonly Faced Issues

We list down some ***commonly-encountered issues*** you might face while setting up our project, along with our suggested solutions.

1. Encountering error `chown: changing ownership of /home/vagrant/csmodify: Not a directory` after running `vagrant up`

    **Solution:** Try reinstalling [VirtualBox](https://www.virtualbox.org/wiki/Downloads) again, then run `vagrant reload`.


2. Unable to run `vagrant ssh` in `cmd` (for Windows users)

    **Solution:** Set your PATH variable using the command `PATH=%PATH%;C:\Program Files\Git\usr\bin`. (**This assumes you already have Git Bash installed on your machine.**)


3. Encountering error `Stderr: VBoxManage.exe: error: VT-x is disabled in the BIOS for all CPU modes (VERR_VMX_MSR_ALL_VMX_DISABLED) VBoxManage.exe: error: Details: code E_FAIL (0x80004005), component ConsoleWrap, interface IConsole` after running `vagrant up`

    **Solution:** Please make sure that your machine supports virtualization.

## Other Issues

Should you face an issue related to the project setup, that you are unable to solve, you can contact us directly on GitHub, or drop us a mail at `nus-dot-csmodify-at-gmail-dot-com`.