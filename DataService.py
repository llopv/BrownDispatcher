import pandas as pd


class DataService:
    def __init__(self, github):
        self.projects = []
        self.github = github
        self.projectIssues = None
        self.userIssues = None

    def fetchUserIssues(self):
        self.userIssues = pd.DataFrame(self.github.getUserIssues())

    def addProject(self, project):
        self.projects.append(project)
        self.projectIssues = pd.DataFrame(self.github.getProjectIssues(project))


    def getIssues(self):
        return (self.projectIssues, self.userIssues)

    def acceptIssue():
        pass

    def rejectIssue():
        pass
