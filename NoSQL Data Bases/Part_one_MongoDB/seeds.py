import json
from models import Authors, Quotes
import connect


def find_id(class_name, name: str):
    """
    Find ID by name

    :param class_name: class Document
    :param name: str
    :return: str
    """
    return [_.id for _ in class_name.objects(fullname=name)][0]


if __name__ == '__main__':

    with open("authors.json", 'r', encoding="utf-8") as file:
        for dict_data in json.load(file):
            fullname = dict_data.get('fullname')
            born_date = dict_data.get('born_date')
            born_location = dict_data.get('born_location')
            description = dict_data.get('description')
            Authors(fullname=fullname, born_date=born_date, born_location=born_location, description=description).save()
            print(f'{fullname=}, {born_date=}, {born_location=}, {description=}')

    with open("quotes.json", 'r', encoding="utf-8") as file:
        for dict_data in json.load(file):
            tags = dict_data.get('tags')
            author = find_id(Authors, dict_data.get('author'))
            quote = dict_data.get('quote')
            Quotes(tags=tags, author=author, quote=quote).save()
