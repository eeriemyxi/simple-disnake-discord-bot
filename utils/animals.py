import httpx
from urllib.parse import quote, quote_plus
class Animals():
    def __init__(self, name: str) -> str:
        self.animals = ('dog', 'cat', 'panda', 'fox', 'red_panda', 'koala', 'bird', 'raccoon', 'kangaroo')
        self._checker(name)
        self.name = name.lower()
        
    def _url_fix(self, url):
        return quote_plus(url)

    def _checker(self, animal_name):
        if not animal_name in self.animals:
            raise NameError('Unknown animal name')

    async def fact(self):
        async with httpx.AsyncClient() as client:
            source = await client.get(f'https://some-random-api.ml/animal/{self.name}')
            return source.json().get('fact')

    async def image(self):
        async with httpx.AsyncClient() as client:
            source = await client.get(f'https://some-random-api.ml/animal/{self.name}')
            return source.json().get('image')
    