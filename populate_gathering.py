import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'data_web.settings')

import django
django.setup()

from gathering.models import DataTable, UserProfile, DataTableOwner, DataTableItem
from django.contrib.auth.models import User

def populate ():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.
    datatable_items1 = [
        {'order_num': 1, 'content': '小明,19,04051401,广东'},
        {'order_num': 2, 'content': '小芳,17,04051402,沈阳'},
        {'order_num': 3, 'content': '小东,21,04051404,陕西'},
    ]

    datatable_items2 = [
        {'order_num': 1, 'content': '小明,19,04051401,广东,93'},
        {'order_num': 2, 'content': '小芳,17,04051402,沈阳,88'},
        {'order_num': 3, 'content': '小东,21,04051404,陕西,90'},
    ]

    datatables = [
        {'serial_key': '1111',
         'name': 'First Table',
         'head': 'name,age,class,hometown',
         'sample': 'Mary,16,04051401,NewYork',
         'datatable_items': datatable_items1},
        {'serial_key': '2222',
         'name': 'Second Table',
         'head': 'name,age,class,hometown,grade',
         'sample': 'Mary,16,04051401,NewYork, 100',
         'datatable_items': datatable_items2},
    ]

    tableowner = [
        {'datatables': datatables}
    ]


    for d in datatables:
        datatable = add_datatable_to(d, 'kermit')
        for item in d['datatable_items']:
            add_items_to_table(datatable, item)


def add_datatable_to (datatable, username):
    owner = DataTableOwner.objects.get_or_create(user=User.objects.get_by_natural_key(username=username))[0]
    owner.name = username
    owner.save()
    table, created = DataTable.objects.get_or_create(owner=owner, serial_key=datatable['serial_key'])
    table.name = datatable['name']
    table.head = datatable['head']
    table.sample = datatable['sample']
    table.save()
    return table

def add_items_to_table (datatable, datatable_item):
    item = DataTableItem.objects.get_or_create(datatable=datatable, content=datatable_item['content'])[0]
    item.order_num = datatable_item['order_num']
    item.save()
    return item


#start execution here
if __name__ == '__main__':
    print('Staring rango population script...')
    populate()
