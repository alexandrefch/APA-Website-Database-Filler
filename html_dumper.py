import requests
from bs4 import BeautifulSoup


class HtmlDumper:
    @staticmethod
    def html_to_string(child):
        res = ''
        for element in child:
            res = res + (element.string or str(element)).lower().strip().replace('\'', '\\\'')
        return res

    @staticmethod
    def dump_page(url):
        dumped_info = dict()
        request = requests.get(url)
        html_page = BeautifulSoup(request.text, 'html.parser')
        table = html_page.find('table', {'class': 'table table-striped table-hover'})

        for tr in table.findAll('tr'):
            for td in tr.findAll('td'):
                child = td.findAll()
                if len(child) >= 2:
                    name = child[0].string
                    value = HtmlDumper.html_to_string(child[1:])

                    for key in ['Discipline', 'Pathologies / Prévention', 'Public', 'Lieu de pratique']:
                        if name == key:
                            value = [x.lower().strip() for x in value.split(',')]

                    dumped_info[name] = value

        return dumped_info
