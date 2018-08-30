import configparser
import sys
from GithubService import GithubService
from DataService import DataService

config = configparser.ConfigParser()
config.read("config")
try:
  user = config['Credentials']['user']
  password = config['Credentials']['pass']
except KeyError:
  print("Config file needed. Please, copy and fill config-default.")
  sys.exit()

data = DataService(GithubService(user, password))
#data.addProject('ipfs/go-ipfs')
data.fetchUserIssues()
projectIssues, userIssues = data.getIssues()
print(projectIssues)
#projectIssues.to_csv("projectIssues.csv")
print(userIssues)
userIssues.to_csv("userIssues.csv")
