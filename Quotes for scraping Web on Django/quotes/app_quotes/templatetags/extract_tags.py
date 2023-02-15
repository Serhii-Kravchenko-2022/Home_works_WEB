from django import template

register = template.Library()


def tags(tag):
    """
    Тут ми реєструємо спеціальний тег для шаблону tags. Всередині однойменної функції ми отримуємо параметр tag
    який буде відображенням quote.tags для нашої нотатки. Всередині функції ми отримуємо список тегів і
     формуємо необхідний нам рядок: усі теги нотатки через кому.
    :param tag: str
    :return: list
    """
    return tag.replace('[', '').replace(']', '').replace("'", '').split(',')


register.filter('tags', tags)
