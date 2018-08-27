import configparser
import sys

config = configparser.ConfigParser()
config.read("config")
try:
  user = config['Credentials']['user']
  password = config['Credentials']['pass']
except KeyError:
  print "Config file needed. Plese, copy and fill config-default."
  sys.exit()
print(user, password)
