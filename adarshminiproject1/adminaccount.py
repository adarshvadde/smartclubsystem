from .models import *
from bson.objectid import ObjectId
def adminaccount(id):
    acc=StudentAccounts.objects.filter(_id=id).values_list('firstname','lastname','admin')
    data={'name':acc[0]+acc[1],'admin':acc[0][2]}
    print(data)
    