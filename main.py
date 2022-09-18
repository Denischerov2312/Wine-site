import datetime
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


FOUNDATION_YEAR = 1920


def get_working_years(foundation_year):
    current_year = datetime.datetime.now().year
    return current_year - foundation_year


def get_excel_data(file):
    excel_data = pandas.read_excel(file, sheet_name='Лист1')
    return excel_data.to_dict(orient='records')


def determine_year(number):
    last_number = int(str(number)[-1])
    last_two_number = int(str(number)[-2:])
    if last_number in range(1, 5) and last_two_number not in range(11, 20):
        if last_number == 1:
            return 'год'
        return 'года'
    return 'лет'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
         )
    template = env.get_template('template.html')

    working_year = get_working_years(FOUNDATION_YEAR)
    drinks = get_sort_drinks('wine.xlsx')
    rendered_page = template.render(
        sub_title=f'Уже {working_year} {determine_year(working_year)} с вами',
        drinks=drinks              
                   )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def get_sort_drinks(file):
    excel_data = pandas.read_excel(file,
                                   sheet_name='Лист1',
                                   na_values='a',
                                   keep_default_na=False
                                   )
    drinks_with_category = collections.defaultdict(list)
    drinks = excel_data.to_dict(orient='records')
    for drink in drinks:
        drinks_with_category[drink['Категория']].append(drink)
    return(drinks_with_category)


if __name__ == '__main__':
    main()