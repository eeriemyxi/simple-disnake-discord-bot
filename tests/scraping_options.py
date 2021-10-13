import aiohttp, asyncio, requests
from bs4 import BeautifulSoup
import re
def _scraper(source, query):
    soup = BeautifulSoup(source, "html.parser")
    search_list = soup.find("dt", attrs={"id": query})
    if search_list is None:
        return (404, "No definition was found for {}".format(query))
    codeblock = search_list.parent.find("dt")
    operations = search_list.parent.find('div', attrs = {'class':'operations docutils container'})
    print(operations)
    operations_string = []
    if operations is not None:
        o = operations.find_all('dl', attrs = {'class':'describe'})
        for i in o:
            operations_string.append(('**`{}`**'.format(i.dt.text.strip('\n')), f'> {i.dd.text}'))
        print(
            '\n'.join([name+'\n'+desc for name, desc in operations_string])
        )

    # operations = 'Supported operations:\n'+operations.text if operations else ''
    final_string = "```py\n{}```\n{}".format(codeblock.text,operations)
    return (200, re.sub(r'\n\s*\n', '\n\n', final_string))

hi = _scraper(requests.get('https://disnake.readthedocs.io/en/latest/api.html?').text, 'disnake.Embed')
print(hi)
