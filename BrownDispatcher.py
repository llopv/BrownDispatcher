import configparser
import sys
from github import Github
import githubConnector

config = configparser.ConfigParser()
config.read("config")
try:
  user = config['Credentials']['user']
  password = config['Credentials']['pass']
except KeyError:
  print("Config file needed. Please, copy and fill config-default.")
  sys.exit()
#print(user, password)

g = githubConnector.connect(user, password)

print ("Proyects that "+ user + " collaborates with:")
githubConnector.show_projects(g)
