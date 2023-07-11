from .models import *
from bson.objectid import ObjectId

def clubsaccount(cb,id):
    club=ClubsAccounts.objects.filter(club=cb).values_list('studentobjectid')
    accountlist=[]
    for ids in club:
        try:
            acc=StudentAccounts.objects.filter(_id=ObjectId(ids[0])).values_list('firstname','lastname','profile_img','rollno','_id','email')
            for allacc in acc:
                accountlist.append({'name':allacc[0]+allacc[1],'profile':allacc[2],'rollno':allacc[3],'profile_img':'/'+id+'/'+str(allacc[4])})
        except:
            acc=AdminAccounts.objects.filter(_id=ObjectId(ids[0])).values_list('firstname','lastname','profile_img','rollno','_id','email')
            for allacc in acc:
                accountlist.append({'name':allacc[0]+allacc[1],'profile':allacc[2],'rollno':allacc[3],'profile_img':'/'+id+'/'+str(allacc[4])})
       
            
    return accountlist