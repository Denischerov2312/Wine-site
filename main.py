import os
import datetime
import collections
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv


def get_operating_years():
    foundation_year = 1920
    current_year = datetime.datetime.now().year
    return current_year - foundation_year


def determine_year(number):
    last_number = int(str(number)[-1])
    last_two_number = int(str(number)[-2:])
    if last_number == 1:
        return 'год'
    elif last_number in range(2, 5) and last_two_number not in range(11, 20):
        return 'года'
    return 'лет'

def get_drinks_filepath():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', help='Путь до xl файла с напитками', default='wine.xlsx')
    args = parser.parse_args()
    return args.file


def get_sorting_drinks(filepath):
    excel_data = pandas.read_excel(filepath,
                                   sheet_name='Лист1',
                                   na_values='a',
                                   keep_default_na=False
                                   )
    drinks_with_category = collections.defaultdict(list)
    drinks = excel_data.to_dict(orient='records')
    for drink in drinks:
        drinks_with_category[drink['Категория']].append(drink)
    return drinks_with_category


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
         )
    template = env.get_template('template.html')

    operating_years = get_operating_years()
    drinks = get_sorting_drinks(get_drinks_filepath())
    rendered_page = template.render(
        sub_title=f'Уже {operating_years} {determine_year(operating_years)} с вами',
        drinks=drinks              
                   )

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    print(determine_year(125))
