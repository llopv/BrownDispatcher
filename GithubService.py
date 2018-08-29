from github import Github

class GithubService:
    def __init__(self, user, password):
        #  create the Github API instance
        self.g = Github(user, password)

    def getUserIssues(self, username):
        for repo in self.g.get_user().get_repos():
            for issue in repo.get_issues():
                for comment in issue.get_comments():
                    if comment.user.login == username:
                        print(repo.name + " - " +issue.title + " - " + issue.html_url)
                        break
