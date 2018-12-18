import configparser

class Config:
    """Reads the config file and fetches the github username and password and the
    name of the project we would like to receive the recomendations.
    """
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config")
        try:
            self.user = config['Credentials']['user']
            self.password = config['Credentials']['pass']
            self.project = config['Project']['name']
        except KeyError:
            raise Exception("Config file needed or malformed. Please, copy and fill config-default.")

    def getConfig(self):
        """Returns the Github username and password and the project name we want to get recommendations from.
        """
        return (self.user, self.password, self.project)
