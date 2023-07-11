from .models import *
from bson.objectid import ObjectId

def allaccount(dp,id):
    acc=StudentAccounts.objects.filter(department=dp).values_list('firstname','lastname','profile_img','rollno','_id','email')
    accountlist=[]
    emaillist=[]
    for allacc in acc:
        accountlist.append({'name':allacc[0]+allacc[1],'profile':allacc[2],'rollno':allacc[3],'profile_img':'/'+id+'/'+str(allacc[4])})
    for emails in acc:
        emaillist.append(emails[5])
    return emaillist,accountlist