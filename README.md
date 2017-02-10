# cs-modify

App structure:

1. app.py
  * The application's home file
2. /components
  * Contains all logical components
3. /public
  * This folder is split into:
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