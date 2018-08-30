from github import Github
import time

class GithubService:
    def __init__(self, user, password):
        #  create the Github API instance
        self.github = Github(user, password)

    def getUserIssues(self):
        issues = []
        user = self.github.get_user().login
        for issue in self.github.search_issues("involves:%s type:issue"%(user)):
            print(issue.title)
            issues.append(self._issueToDict(issue))
        return issues

    def getProjectIssues(self, projectName):
        issues = []
        repo = self.github.get_repo(projectName)
        for issue in repo.get_issues(state='open'):
            issues.append(self._issueToDict(issue))
        return issues

    def _issueToDict(self, issue):
        labels = [label.name for label in issue.labels]
        comments = {}
        for c in issue.get_comments():
            try:
                comments[c.user.login] += 1
            except KeyError as e:
                comments[c.user.login] = 1

        return {
            "repo": issue.repository.name,
            "title": issue.title,
            "body": issue.body,
            "labels": labels,
            "state": issue.state,
            "url": issue.html_url,
            "created_at": issue.created_at,
            "updated_at": issue.updated_at,
            "user": issue.user.login,
            "comments": comments
        }
