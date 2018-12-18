from DataService import DataService
from RecommenderEngine import RecommenderEngine
from Server import Server

data = DataService()
recommender = RecommenderEngine(data)
server = Server(data, recommender)
server.run()
