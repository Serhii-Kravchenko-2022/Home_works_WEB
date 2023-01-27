from mongoengine import Document, StringField, ReferenceField, ListField, CASCADE


class Authors(Document):
    fullname = StringField(max_length=150, required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=20))
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
