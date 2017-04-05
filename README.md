# CSModify: A Module Planner for Module Administrators in NUS School of Computing (SoC)

## Contents

* [About the Project](#about-the-project)
* [Downloading the Project Files](#downloading-the-project-files)
* Setup
  * [With Vagrant](#with-vagrant)
  * [Without Vagrant](#without-vagrant)
* [Project Files & Structures](#project-files--structure)
* [Building and Running in Development Mode](#building-and-running-in-development-mode)
* [Building and Running in Production Mode](#building-and-running-in-production-mode)
* [About Us](#about-us)
* [License](#license)

## About the Project

CSModify is a web application that displays data visualizations and simulate module changes, to assist in module planning for NUS School of Computing (SoC).

Module planning is a process where module administrators make various decisions for modules. Some examples would be deciding which modules should be mounted/dismounted for a particular Academic Year-Semester (denoted as an AY-Sem), determining the quota that should be allocated to a module, or finding out how many students will be affected should a module be taken down in a particular AY-Sem.

Module planning itself is, by no means, an easy feat. As there is no central system for doing this currently, what this project aims to do would be to assist module planners by showing data visualizations of their queries in a manner that is easy to process. By doing so, we hope that they will be able to make decisions regarding module planning with greater convenience and ease.

## Downloading the Project Files

Our project files are located in the [CSModify repository](https://github.com/nus-mtp/cs-modify). You can either fork our repository to obtain the project files, or download the zip files from there.

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
    * The settings for these 2 files should match
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

First, set `web.config.debug` to `True` in `app.py`, which will allow the stack trace to be displayed upon the app's failure. Once this is done, you can view your app by running `python app.py` and accessing it on `localhost:8080`.

Next:

**For Vagrant users:** Make sure both `bootstrap.sh` in `/vagrant_setup` and `local_database_data.py` in `/components` are modified accordingly, so that the app can connect to your database. This should have already been done while you were setting up the project.

**For non-Vagrant users:** Make sure that `local_database_data.py` in `/components` is modified accordingly, so that the app can connect to your database. Instructions on how to do so are included directly inside the file itself.

## Building and Running in Production Mode

Simply set `web.config.debug` to `False`, and you are ready to push your app out for production. You can then choose to deploy this app to the deployment platform that you desire.

To access the app, you can just access the URL where your app is deployed to.

## About Us

We at Team Lezzgo are students of NUS School of Computing.

Do contact us on GitHub if you want to talk to us about this project!

### Members

* [GQ](https://github.com/tgqiang)
* [Nic](https://github.com/nlzz22)
* [QX](https://github.com/helloqx)
* [Rufus](https://github.com/xaterz)
* [XiaoXiao](https://github.com/a0129998)

## License

This project is licensed under the MIT License.