import deta
import dotenv
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode

dotenv.load_dotenv()


class DocsCaching():
    def __init__(self):
        self.db = deta.Deta(os.getenv("DETAPROJECTKEY")).Base("docs_cache")

    def is_cached(self, query: str):
        """
        Check if query is in cache. If it is in cache, it returns it.
        """
        return cache if (cache := self.db.get(query)) else False
    
    def cache(self, query, data):
        '''
        Cache query and its result.
        if it is already in cache, It doesn't

        Parameters
        ----------
        query: definition
        data: Description of the definition
        '''
        if self.is_cached(query):
            return
        self.db.put(data, query)
        return
    
    def get_cache(self, query):
        '''
        Get query from cache. If it is not cached, it will raise `ValueError`.
        '''
        if (cache := self.is_cached(query)):
            return cache
        raise ValueError

