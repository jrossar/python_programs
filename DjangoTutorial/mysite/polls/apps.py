from django.apps import AppConfig


#add dotted path to settings.py ie. polls.apps.PollsConfig
#python manage.py makemigrations polls (tells django you made changes to models)
#migrations are how django stores changes to your models
class PollsConfig(AppConfig):
    name = 'polls'
