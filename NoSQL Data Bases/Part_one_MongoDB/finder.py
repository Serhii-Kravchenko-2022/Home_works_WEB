import redis
from redis_lru import RedisLRU

from models import Authors, Quotes
import connect

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def get_data(string: str):
    com = string.split(':')[0].strip() if len(string.split(':')) > 1 else string.strip()
    val = string.split(':')[1].strip() if len(string.split(':')) > 1 else ''
    return com, val


@cache
def get_quotes_by_name(value: str):
    """
    Find quotes by authors name

    :param value: str
    :return: tuple of quotes.object, str
    """
    value = value.capitalize()
    author_id = [_.id for _ in Authors.objects(fullname__regex=value)][0] \
        if Authors.objects(fullname__regex=value) else ''
    if not author_id:
        print(f"Author {value} is not exist")
        quotes = []
        result_string = f"Author {value} is not exist"
        return quotes, result_string
    quotes = Quotes.objects(author=author_id)
    result_string = f"{value}'s quote('s) is:"
    return quotes, result_string


@cache
def get_quotes_by_tag(value: str):
    """
    Find quotes by tag

    :param value:
    :return: tuple of quotes.object, str
    """
    quotes = Quotes.objects(tags__regex=value) if Quotes.objects(tags__regex=value) else []
    result_string = f"For tag {value} quote('s) is:" if quotes else f"Tag {value} is not exist"
    return quotes, result_string


@cache
def get_quotes_by_tags(value: str):
    """
    Find quotes by tags

    :param value:
    :return: tuple of quotes.object, str
    """
    tags = ",".join(x.strip() for x in value.split(',')).split(',')
    quotes = Quotes.objects(tags__in=tags) if Quotes.objects(tags__in=tags) else []
    result_string = f"For tag's {tags} quote('s) is:" if quotes else f" Tags {tags} is not exist"
    return quotes, result_string


if __name__ == '__main__':
    while True:
        input_string = input('[+]Input command: ').lower()
        command, value = get_data(input_string)
        match command:
            case 'name':
                quotes, result_string = get_quotes_by_name(value)
            case 'tag':
                quotes, result_string = get_quotes_by_tag(value)
            case 'tags':
                quotes, result_string = get_quotes_by_tags(value)
            case 'exit':
                print('[-]Goodbye')
                break
            case _:
                print('[-]Unknown command. Try again')
                continue
        print(result_string)
        if quotes:
            [print('[-]', _.quote) for _ in quotes]
