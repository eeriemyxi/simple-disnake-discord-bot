import httpx
class Animals():
    def __init__(self, name: str) -> str:
        self.animals = ('dog', 'cat', 'panda', 'fox', 'red_panda', 'koala', 'bird', 'raccoon', 'kangaroo')
        self._checker(name)
        self.name = name.lower()

    def _checker(self, animal_name: str) -> str:
        '''
        Checks if `animal_name` is from `self.animals`
        '''
        if not animal_name in self.animals:
            raise NameError('Unknown animal name')

    async def fact(self) -> str:
        '''
        Returns a random fact about the animal
        '''
        async with httpx.AsyncClient() as client:
            source = await client.get(f'https://some-random-api.ml/animal/{self.name}')
            return source.json().get('fact')

    async def image(self) -> str:
        '''
        Returns a random image of the animal
        '''
        async with httpx.AsyncClient() as client:
            source = await client.get(f'https://some-random-api.ml/animal/{self.name}')
            return source.json().get('image')
    