import configparser
import sys
from github import Github

config = configparser.ConfigParser()
config.read("config")
try:
  user = config['Credentials']['user']
  password = config['Credentials']['pass']
except KeyError:
  print("Config file needed. Plese, copy and fill config-default.")
  sys.exit()
print(user, password)

g = Github(user, password)

for repo in g.get_user().get_repos():
  print(repo.name)
