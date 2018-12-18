from flask import Flask, redirect

class Server(object):
    """HTTP server to display the top 10 recommended issues to the user and offer
    her a way to accept and reject them. This class represents the view in the
    MVC design.

    Args:
        data (obj): Instance of DataService in order persist acceptance and
        rejection of issues.
        recommender (obj): Instance of RecommenderEngine in order to retreive
        the top 10 shown to the user.
    """
    def __init__(self, data, recommender):
        self.data = data
        self.recommender = recommender
        self.app = Flask('brown dispatcher')

        @self.app.route('/')
        def root():
            top10 = self.recommender.getTop10()
            s = "<h1>Brown Dispatcher</h1><ol>"
            for index, row in top10.iterrows():
                s += "<li><a target='_blank' href='" + row['url'] + "'>" + row['title'] + "</a> <a href='/accept/"+str(index)+"'>" + u"\u2714" + "</a> <a href='/reject/"+str(index)+"'>" + u"\u2717" + "</a></li>"
            s += "</ol>"
            return s

        @self.app.route('/accept/<id>')
        def accept(id):
            data.acceptIssue(int(id))
            return redirect('/')

        @self.app.route('/reject/<id>')
        def reject(id):
            data.rejectIssue(int(id))
            return redirect('/')

    def run(self):
        self.app.run()
