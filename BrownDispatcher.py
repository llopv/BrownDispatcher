import configparser
config = configparser.ConfigParser()
config.read("config")
user = config['Credentials']['user']
password = config['Credentials']['pass']

print(user, password)
