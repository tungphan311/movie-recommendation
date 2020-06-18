# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


# %%
class CF(object):
    def __init__(self, Y_data, k, dist_func = cosine_similarity):
        self.Y_data = Y_data
        self.k = k
        self.dist_func = dist_func
        self.Ybar_data = None
        
        # number of users and items. plus 1 cuz id start with 0
        self.n_users = int(np.max(self.Y_data[:, 0])) + 1
        self.n_items = int(np.max(self.Y_data[:, 1])) + 1
    
    def normalize_Y(self):
        users = self.Y_data[:, 0] # first col of matrix
        self.Ybar_data = self.Y_data.copy()
        self.mu = np.zeros((self.n_users,))
        
        for n in range(self.n_users):
            ids = np.where(users == n)[0].astype(np.int32)
            
            # get all item which user with ids already rated and rating values.
            item_ids = self.Y_data[ids, 1]
            ratings = self.Y_data[ids, 2]
            
            # take mean 
            m = np.mean(ratings)
            if np.isnan(m):
                m = 0 # to avoid empty array an non value
            
            # store average rating of each user
            self.mu[n] = m
                
            # normalize
            self.Ybar_data[ids, 2] = ratings - self.mu[n]
            
        self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2], (self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))
        self.Ybar = self.Ybar.tocsr()
        
    def similarity(self):
        self.S = self.dist_func(self.Ybar.T, self.Ybar.T)
        
    def refresh(self):
        """
        Normalize data and calculate similarity matrix again (after
        some few ratings added)
        """
        self.normalize_Y()
        self.similarity() 
        
    def fit(self):
        self.refresh()
        
    def __pred(self, u, i, normalized = 1):
        # find all user whos rated i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        
        # find similarity btw the current user and others who already rated i
        sim = self.S[u, users_rated_i]
                
        # find the k most similar users
        a = np.argsort(sim)[-self.k:]
        
        # and the corresponding similarity lvl
        nearest_s = sim[a]
        
        r = self.Ybar[i, users_rated_i[a]]
        
        if normalized:
            # add a small number, for instance, 1e-8, to avoid dividing by 0
            return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8)

        return (r*nearest_s)[0]/(np.abs(nearest_s).sum() + 1e-8) + self.mu[u]
    
    def pred(self, u, i, normalized = 1):
        """ 
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        return self.__pred(u, i, normalized)
    
    def recommend(self, u, normalized = 1):
        ids = np.where(self.Y_data[:, 0] == u)[0]
        
        item_rated_by_u = self.Y_data[ids, 1].tolist()
        
        recommend_items = []
        
        for i in range(self.n_items):
            if i not in item_rated_by_u:
                rating = self.__pred(u, i)
                
                if rating > 0:
                    recommend_items.append(i)
                    
        # sort list recommend from highest predicted rating to lowest
        # recommend_items.sort(key=lambda tup: tup[1], reverse=True)
        
        return recommend_items
    
    def print_recommendation(self, u):
        """
        print all items which should be recommended for each user 
        """
        print('Recommendation: ')
        # for u in range(self.n_users):
        recommended_items = self.recommend(u)
        print('    Recommend item(s):', recommended_items[:5], 'to user', u)


# # %%
# r_cols = ['userId', 'movieId', 'rating', 'timestamp']


# %%
# ratings = pd.read_csv('dataset/ratings.csv', sep=',', encoding='latin-1')
# # ratings_test = pd.read_csv('C:/Users/ad/Desktop/ml-100k/ub.test', sep='\t', names=r_cols, encoding='latin-1')

# ratings['rating'] = ratings['rating'].apply(lambda x: int(round(x)))

# rate_train = ratings.to_numpy(dtype="Int64")

# # indices start from 0
# rate_train[:, :2] -= 1

# # %%
# rs = CF(rate_train, k = 30)
# rs.fit()

# rs.print_recommendation(1)


# # %%
# n_tests = rate_test.shape[0]
# SE = 0 # squared error
# for n in range(n_tests):
#     pred = rs.pred(rate_test[n, 0], rate_test[n, 1], normalized = 0)
#     SE += (pred - rate_test[n, 2])**2 

# RMSE = np.sqrt(SE/n_tests)
# print('User-user CF, RMSE =', RMSE)
