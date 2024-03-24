import configparser

# create a ConfigParser object and read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# get the values from the configuration file
host = config.get('Database', 'host')
port = config.get('Database', 'port')
user = config.get('Database', 'user')
password = config.get('Database', 'password')
database = config.get('Database', 'database')

# use the configuration values in your code
print(f"Connecting to database {database} at {host}:{port} as user {user} with password {password}")