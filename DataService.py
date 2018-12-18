from Config import Config
from GithubService import GithubService
import pandas as pd

class DataService:
    """This class fetches, saves, and loads the data of the issues into pandas'
    data frames. The data is saved in CSV format under the userIssues.csv and
    projectIssues.csv files. This class represents the model in the MVC design.
    """
    def __init__(self):
        self.projectIssues = None
        self.userIssues = None

    def _fetchUserIssues(self, github):
        self.userIssues = pd.DataFrame(github.getUserIssues())
        self.userIssues.to_csv("userIssues.csv")

    def _fetchProjectIssues(self, github, project):
        self.projectIssues = pd.DataFrame(github.getProjectIssues(project))
        self.projectIssues.to_csv("projectIssues.csv")

    def _loadUserIssues(self):
        self.userIssues = pd.read_csv('userIssues.csv')

    def _loadProjectIssues(self):
        self.projectIssues = pd.read_csv('projectIssues.csv')

    def getIssues(self):
        """If the issue files (userIssues.csv and projectIssues.csv) are present
        in the filesystem, we load their data and return the data frames. If they
        are not present, we check out the config file in order to obtain the
        github username and password and the project, and we fetch the issues
        using the GithubService class. If either the the issue files and the
        config file are not present, an exception is raised.

        Returns:
            Two data frames, the first with the project issues that can be
            recommended to the user, and the second with the user issues used to
            train the system. The two sets are exclusive (we erase the issues
            that are present in projectIssues due we should not recommend an
            issue in which the user is already participating).
        """
        try:
            self._loadUserIssues()
            self._loadProjectIssues()
        except:
            config = Config()
            user, password, project = config.getConfig()
            github = GithubService(user, password)
            self._fetchUserIssues(github)
            self._fetchProjectIssues(github, project)

        # We don't want to recommend issues in which user is already participating, so projectIssues = projectIssues - userIssues
        self.projectIssues = pd.concat([self.projectIssues, self.userIssues, self.userIssues], sort=True).drop_duplicates(keep=False)
        return (self.projectIssues, self.userIssues)

    def acceptIssue(self, id):
        """Accepts an issue from the projectsIssues set, so we don't recommend
        it anymore but it is used by the system to recommend other similar issues.

        Args:
            id (int): Index inside projectIssues list
        """
        issue = self.projectIssues[id:id+1]
        self.userIssues = pd.concat([issue, self.userIssues], ignore_index=True, sort=True)
        self.projectIssues = self.projectIssues.drop(issue.index)
        self.userIssues.to_csv("userIssues.csv")
        self.projectIssues.to_csv("projectIssues.csv")

    def rejectIssue(self, id):
        """Rejects an issue from the projectsIssues set, so we don't recommend
        it anymore.

        Args:
            id (int): Index inside projectIssues list
        """
        issue = self.projectIssues[id:id+1]
        self.projectIssues = self.projectIssues.drop(issue.index)
        self.projectIssues.to_csv("projectIssues.csv")
