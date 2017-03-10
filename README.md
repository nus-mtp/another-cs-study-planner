# cs-modify

## App structure:

1. app.py
  * The application's home file
2. /components
  * Contains all logical components
  * This folder contains:
    * /handlers (for py file to handle web requests)
3. /static
  * This folder is split into:
    * /fonts (for storing glyphicons)
    * /stylesheets (for CSS resources)
    * /javascripts (for JS scripts)
    * /images (for storing image files)
4. /templates
  * Contains all web.py template files
5. /test
  * Contains all test cases
6. /utils
  * Contains internal scripts
7. .travis.yml
  * For building the app environment in Travis CI
8. Procfile
  * For defining which python file to run in Heroku
9. requirements.txt
  * For defining app requirements in Heroku
10. README.md

## How to create local\_database_data.py manually ?

In order to run our code in your local computer, you would be
required to have Postgres installed ([link](https://www.postgresql.org/download/))
and manually create the local\_database_data.py file (see steps below)

1. Create a file named "local\_database_data.py" inside your `components/` folder.
2. Write this inside your file `local_database_data.py`:


```
    database_name = '<your_database_name>' # Replace with your postgres database name
    user_name = '<your_user_name>'         # Replace with your postgres username
    password = '<your_password>'           # Replace with your postgres password
    host_name = 'localhost'  
    port = '<your_port_number>'            # Replace with the port number used by postgres
    
    def get_database_name():
          return database_name

    def get_user_name():
          return user_name

    def get_password():
          return password

    def get_host_name():
          return host_name

    def get_port():
          return port
```