import configparser
import sys
from github import Github
from GithubService import GithubService

config = configparser.ConfigParser()
config.read("config")
try:
  user = config['Credentials']['user']
  password = config['Credentials']['pass']
except KeyError:
  print("Config file needed. Please, copy and fill config-default.")
  sys.exit()

g = GithubService(user, password)
g.getUserIssues(user)
