import deta
import dotenv
import os

dotenv.load_dotenv()


class DocsCaching:
    def __init__(self):
        self.db = deta.Deta(os.getenv("DETAPROJECTKEY")).Base("docs_cache")

    def is_cached(self, query: str):
        """
        Check if query is in cache. If it is in cache, it returns it.
        """
        return cache if (cache := self.db.get(query)) else False

    def cache(self, query: str, desc: str, force: bool = False):
        """
        Cache query and its result.
        if it is already in cache, It doesn't

        Parameters
        ----------
        query: :class:`str`
            Name of the definition class
        desc: :class:`str`
            Description of the definition
        force: :class:`bool`
            If it's `True`, it will replace the key with the passed data even if it's already in the DB.
        """
        if self.is_cached(query) and force == False:
            return
        self.db.put(desc, query)
        return

    def get_cache(self, query):
        """
        Get query from cache. If it is not cached, it will raise `ValueError`.
        """
        if cache := self.is_cached(query):
            return cache.get('value')
        raise ValueError