# The password variable is provided, for convenience.
DB_USER_PASSWORD='12345678'

echo ""
echo ""
echo "==================== [ INSTALLING ESSENTIALS ] ===================="
sudo apt-get update
sudo apt-get install build-essential

echo ""
echo ""
echo "==================== [ INSTALLING PYTHON & PIP ] ===================="
sudo apt-get install python-dev python-pip -q -y

echo ""
echo ""
echo "==================== [ INSTALLING POSTGRESQL ] ===================="
sudo apt-get install -y postgresql postgresql-client postgresql-contrib libpq-dev

echo ""
echo ""
echo "==================== [ INSTALLING PYTHON DEPENDENCIES ] ===================="
sudo pip install --upgrade web.py
sudo pip install --upgrade nose
sudo pip install --upgrade paste
sudo pip install --upgrade psycopg2
sudo pip install --upgrade pylint

# You may wish to modify the shell commands beyond this point
# to re-configure the database settings as desired.
# 
# By default, we use the 'postgres' user.
# If your 'postgres' user requires password access, you may modify the DB_PASSWORD variable.
# 
# If you use another user for your PostgreSQL database, please make sure you add your own
# command to create the user.
echo ""
echo ""
echo "==================== [ CONFIGURING DATABASE USER ] ===================="
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$DB_USER_PASSWORD';"
