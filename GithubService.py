from github import Github
import time

class GithubService:
    """"GithubService connects with the Github API in order to fetch the issues
    required by the program. It fetches the issues in which the user is involved
    and the open issues of an specific project.

    Attributes:
        user (str): Github username
        password (str): Github password
    """
    def __init__(self, user, password):
        #  create the Github API instance
        self.github = Github(user, password)

    def getUserIssues(self):
        """Fetches all the issues in which a user is involved (max 500).

        Returns:
            A list of dictionaries containing useful information from the issues
        """
        issues = []
        # Github username
        user = self.github.get_user().login
        for issue in self.github.search_issues("involves:%s type:issue"%(user)):
            print(issue.title)
            issues.append(self._issueToDict(issue))
        return issues

    def getProjectIssues(self, projectName):
        """Fetches all the open issues of a project (max 500).

            Args:
                projectName (str): Name of the project as it appears on github,
                such as 'ipfs/go-ipfs'.

            Returns:
                A list of dictionaries containing useful information from the issues
            """
        issues = []
        repo = self.github.get_repo(projectName)
        for issue in repo.get_issues(state='open'):
            print(issue.title)
            issues.append(self._issueToDict(issue))
        return issues

    def _issueToDict(self, issue):
        """Curate issues in order to make them more manageable

            Args:
                issue (obj): Issue object from the pyGithub library

            Returns:
                A dictionary with the following keys: repo, title, body, labels,
                state, url, created_at, updated_at, users.
        """
        labels = [label.name for label in issue.labels]
        comment_authors = []
        for c in issue.get_comments():
            comment_authors.append(c.user.login)

        return {
            "repo": issue.repository.name,
            "title": issue.title,
            "body": issue.body,
            "labels": ' '.join(labels),
            "state": issue.state,
            "url": issue.html_url,
            "created_at": issue.created_at,
            "updated_at": issue.updated_at,
            "users": issue.user.login + ' ' + ' '.join(comment_authors)
        }
