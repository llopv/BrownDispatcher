import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

class RecommenderEngine:
    """Recommends 10 issues to the user based on the similarity with the top 5
    issues in the userIssues dataset.

    Args:
        data (DataService): Instance of the BrownDispatcher model
    """
    def __init__(self, data):
        # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
        self.tfidf = TfidfVectorizer(stop_words='english')
        # We do not want to down-weight the presence of a label/author if it appears in relatively more issues.
        self.count = CountVectorizer(stop_words='english')
        self.data = data

    def getTop10(self):

        projectIssues, userIssues = self.data.getIssues()
        indices = []

        for idx in range(0,5):
            issues = pd.DataFrame(userIssues[idx:idx+1]).append(projectIssues)
            cosine_sim_body = self.bodySimilarity(issues)
            cosine_sim_authors = self.authorSimilarity(issues)
            cosine_sim_labels = self.labelSimilarity(issues)

            cosine_sim = cosine_sim_body * 0.2 + cosine_sim_authors * 0.4 + cosine_sim_labels * 0.4

            # Get the pairwsie similarity scores of all issues with that issue
            sim_scores = list(enumerate(cosine_sim[0]))

            # Sort the movies based on the similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # Get the scores of the 2 most similar issues
            sim_scores = sim_scores[1:3]

            # Get the issue indices
            indices += [i[0]-1 for i in sim_scores]

        return projectIssues.iloc[indices].drop_duplicates()

    def bodySimilarity(self, issues):
        #Replace NaN with an empty string
        issues['body'] = issues['body'].fillna('')
        #Construct the required TF-IDF matrix by fitting and transforming the data
        tfidf_matrix = self.tfidf.fit_transform(issues['body'])
        # Compute the cosine similarity matrix
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        return cosine_sim

    def authorSimilarity(self, issues):
        #Construct the required count matrix by fitting and transforming the data
        count_matrix = self.count.fit_transform(issues['users'].fillna(''))
        # Compute the cosine similarity matrix
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        return cosine_sim

    def labelSimilarity(self, issues):
        #Construct the required count matrix by fitting and transforming the data
        count_matrix = self.count.fit_transform(issues['labels'].fillna(''))
        # Compute the cosine similarity matrix
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        return cosine_sim
