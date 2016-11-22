import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'data_project.settings')

import django
django.setup()

from gathering.models import DataTable, UserProfile
from django.contrib.auth.models import User

def populate ():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.
    datatables = [
        {'owner': 'kermit',
         'major_id': '1111',
         'minor_id': '1111',
         'name': 'First Table',
         'sample': 'name:Mary,age:16,class:04051401,hometown:NewYork',
         'contents':'小明,19,04051401,广东\n小芳,17,04051402,沈阳\n小东,21,04051404,陕西\n',
        },
        {'owner': 'kermit',
         'major_id': '2222',
         'minor_id': '2222',
         'name': 'second table',
         'sample': 'name:Mary,age:16,class:04051401,hometown:NewYork',
         'contents':'小明,19,04051401,广东\n小芳,17,04051402,沈阳\n小东,21,04051404,陕西\n',
        },
    ]

    for d in datatables:
        add_data_table(d)


def add_data_table (d):
    owner = User.objects.get_by_natural_key(username=d['owner'])
    print(owner.username)
    table, created = DataTable.objects.get_or_create(owner=owner, major_id=d['major_id'], minor_id = d['minor_id'])

    table.name = d['name']
    table.sample = d['sample']
    table.contents = d['contents']
    table.save()

#start execution here
if __name__ == '__main__':
    print('Staring rango population script...')
    populate()
