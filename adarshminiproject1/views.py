from bson.objectid import ObjectId
import os
import re
import base64
import mimetypes
from wsgiref.util import FileWrapper
from pymongo import MongoClient
import gridfs
db = MongoClient().adarshminiproject1
fs = gridfs.GridFS(db)
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from .emailotp import *
from .models import *
from .allaccount import *
from .clubsaccount import *

from django.http.response import  HttpResponse ,StreamingHttpResponse,HttpResponseRedirect  
'''admin=AdminAccounts()
admin.firstname="vadde"
admin.lastname="adarsh"
admin.rollno="20f21a3201"
admin.email="vaddeadarsh150@gmail.com"
admin.department="Data Science"
admin.password="20f21a3201"
admin.admin="admin"
admin.save()'''

Emails=Email()
Otps=Otp()
Emails1=Email1()
Otps1=Otp1()

def home(request):
    updates=Updates.objects.filter(department='home').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'homepage.html',data)
def login(request):
    if request.method=='POST':
        allpost=request.POST
        try:
            logacc=StudentAccounts.objects.filter(rollno=allpost['logrollnumber'],password=allpost['logpassword']).values_list('_id')
            return HttpResponseRedirect('/account/'+str(logacc[0][0]))
        except:
            pass
        try:
            logacc=AdminAccounts.objects.filter(rollno=allpost['logrollnumber'],password=allpost['logpassword']).values_list('_id')
            return HttpResponseRedirect('/account/'+str(logacc[0][0]))
        except:
            pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'loginpage.html',data)
def signin(request):
    if request.method=='POST':
        allpost=request.POST
        allmailslist=[]
        rollnolist=[]
        try:
            allemails=StudentAccounts.objects.values_list('email','rollno')
            for email in allemails:
                allmailslist.append(email[0])
            for rollno in allemails:
                allmailslist.append(rollno[0])
        except:
            pass
        if int(allpost['otp'])==Otps.otprecive()['otp'] and allpost['email']==Emails.Emailrecive()['Email']:
            if allpost['email'] not in allmailslist and allpost['rollnumber'] not in rollnolist :
                ds=StudentAccounts()
                ds.firstname=allpost['firstname']
                ds.lastname=allpost['lastname'] 
                ds.rollno=allpost['rollnumber']
                ds.password=allpost['password']
                ds.email=allpost['email']
                ds.profile_img='/static/clg logo.jpg'
                ds.cover_pic='/static/venu1.jpg'
                ds.department=allpost['department']
                ds.save()
                print('Sucessfully '+allpost['department']+' signin')
                return HttpResponse('Sucessfully ds signin')
            print('email already exist')
            return HttpResponse('email already exist')
    return render(request,'homepage.html')
def signsendemail(request):
    if request.method=='POST':
        allpost=request.POST
        email=allpost['email']
        Emails.Emailsend(email)
        Otps.otpsend(10)
        try:
            subject = 'GatesIT Regestration'
            message = 'Hi '+allpost['firstname'] +' '+allpost['lastname'] +'   Your Regestration code '+str(10)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from,recipient_list)
            print('sucess')
            data='Resend'
            return HttpResponse(data)
        except:
            print('unsucess')
            data='unsucess'
            return HttpResponse(data)
    return render(request,'homepage.html')
def signinotpver(request):
    if request.method=='POST':
        allpost=request.POST
        if int(allpost['otp'])==Otps.otprecive()['otp'] and allpost['email']==Emails.Emailrecive()['Email']:
            print('sucess')
            data="sucess"
            return HttpResponse(data)
    return render(request,'homepage.html')
def forget(request):
    if request.method=='POST':
        allpost=request.POST
        print(allpost)
        loginacc=[]
        try:
            loginacc=StudentAccounts.objects.filter(email=allpost['forgetemail'])
            loginacc.update(password=allpost['password'])
            return HttpResponseRedirect('/')
        except:
             pass
        
    return render(request,'homepage.html')
def forgetsendemail(request):
    if request.method=='POST':
        allpost=request.POST
        email=allpost['email']
        Emails1.Emailsend(email)
        Otps1.otpsend(10)
        try:
            subject = 'GatesIT Forget password'
            message = 'Hi    Your Forget code '+str(10)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from,recipient_list)
            print('sucess')
            data='Resend'
            return HttpResponse(data)
        

        except:
            print('unsucess')
            data='unsucess'
            return HttpResponse(data)
    return render(request,'homepage.html')
def forgetotpver(request):
    if request.method=='POST':
        allpost=request.POST
        if int(allpost['otp'])==Otps1.otprecive()['otp'] and allpost['email']==Emails1.Emailrecive()['Email']:
            print('sucess')
            data="sucess"
            return HttpResponse(data)
    return render(request,'homepage.html')
def logout(request):
    return HttpResponseRedirect('/')
def speech(request):
    if request.method=='POST':
        allpost=request.POST
        print(allpost)
        if allpost['text']=='open. pythonclub.' or allpost['text']=='open python.' or allpost['text']=='open python club.' :
            return HttpResponse('/pythonclub')
        elif allpost['text']=='open. graphicclub.' or allpost['text']=='open graphics.' or allpost['text']=='open graphics club.' :
            return HttpResponse('/graphicclub')
        elif allpost['text']=='open. projectclub.' or allpost['text']=='open project.' or allpost['text']=='open project club.' :
            return HttpResponse('/projectclub')
        elif allpost['text']=='open. euphoriaclub.' or allpost['text']=='open euphoria.' or allpost['text']=='open euphoria club.' :
            return HttpResponse('/euphoriaclub')
        elif allpost['text']=='open. innerwheelclub.' or allpost['text']=='open. innerwheel.' or allpost['text']=='open inner wheel club.' :
           return HttpResponse('/innerwheelclub')
        elif allpost['text']=='open. ideaclub.' or allpost['text']=='open idea.' or allpost['text']=='open idea club.' :
            return HttpResponse('/ideaclub')
        elif allpost['text']=='open. speakingclub.' or allpost['text']=='open. speaking.' or allpost['text']=='open speaking club.' :
            return HttpResponse('/speakingclub')
        elif allpost['text']=='open. codingclub.' or allpost['text']=='open. coding.' or allpost['text']=='open coding club.' :
            return HttpResponse('/codingclub')
        elif allpost['text']=='open. campusradioclub.' or allpost['text']=='open campus radio.' or allpost['text']=='open campusradio club.' :
            return HttpResponse('/campus')
        elif allpost['text']=='open. literacyclub.' or allpost['text']=='open. literacy.' or allpost['text']=='open literacy club.' :
            return HttpResponse('/literacyclub')
        elif allpost['text']=='open datascience.' or allpost['text']=='open ds.' or allpost['text']=='open data science.' :
            return HttpResponse('/datascience')
        elif allpost['text']=='open artifitialintiligence.' or allpost['text']=='open ai.' or allpost['text']=='open artificial intelligence.' :
            return HttpResponse('/cai')
        elif allpost['text']=='open easy e.' or allpost['text']=='open. easy.' or allpost['text']=='open ece.' :
            return HttpResponse('/ece')
        elif allpost['text']=='open eee.' or allpost['text']=='open. eee.' or allpost['text']=='open triple e.' :
            return HttpResponse('/eee')
        elif allpost['text']=='open ce.' or allpost['text']=='open. ce.' or allpost['text']=='open ce' :
            return HttpResponse('/ce')
        elif allpost['text']=='open cs.' or allpost['text']=='open. cs.' or allpost['text']=='open cs' :
            return HttpResponse('/cs')
        elif allpost['text']=='open mech.' or allpost['text']=='open. mech.' or allpost['text']=='open mech' :
            return HttpResponse('/mech')
        elif allpost['text']=='open mba.' or allpost['text']=='open. mba.' or allpost['text']=='open mba' :
            return HttpResponse('/mba')
        elif allpost['text']=='open mca.' or allpost['text']=='open. mca.' or allpost['text']=='open mca' :
            return HttpResponse('/mca')
        elif allpost['text']=='open cse.' or allpost['text']=='open. cse.' or allpost['text']=='open cse' :
            return HttpResponse('/cse')
        elif allpost['text']=='open home.' or allpost['text']=='back to home.' or allpost['text']=='back to home' :
            return HttpResponse('/')
        elif allpost['text']=='open departments.' or allpost['text']=='open. departments.' or allpost['text']=='open departments' :
            return HttpResponse('/departments')
        elif allpost['text']=='open clubs.' or allpost['text']=='open. clubs.' or allpost['text']=='open clubs' :
            return HttpResponse('/clubs')
        elif allpost['text']=='open about.' or allpost['text']=='open. about.' or allpost['text']=='open about' :
            return HttpResponse('/about')
        elif allpost['text']=='open login.' or allpost['text']=='open. login.' or allpost['text']=='open login' :
            return HttpResponse('/login')
        elif allpost['text']=='open placement and training.' or allpost['text']=='open placement. and training.' or allpost['text']=='open. placement. and. training.' :
            return HttpResponse('/trainingandplacement')
        
        return HttpResponseRedirect(allpost['text'])
    
def account(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','rollno')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='home').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'homepage.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='home').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][4]=='admin':
            return render(request,'homepageadmin.html',data)
        else:
            return render(request,'homepage.html',data)
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'homepage.html',data)
     
def departments(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'departments.html',data)
def clubs(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'clubs.html',data)
def about(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'about.html',data)
def trainAplacement(request):
    updates=Updates.objects.filter(department='trainaplace').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'training&placement.html',data)

def datascience(request):
    updates=Updates.objects.filter(department='ds').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'datascience.html',data)
def cse(request):
    updates=Updates.objects.filter(department='cse').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'cse.html',data)
def cai(request):
    updates=Updates.objects.filter(department='cai').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'cai.html',data)
def cs(request):
    updates=Updates.objects.filter(department='cs').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'cs.html',data)
def ce(request):
    updates=Updates.objects.filter(department='ce').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'ce.html',data)
def mech(request):
    updates=Updates.objects.filter(department='mech').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'mech.html',data)
def mba(request):
    updates=Updates.objects.filter(department='mba').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'mba.html',data)
def mca(request):
    updates=Updates.objects.filter(department='mca').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'mca.html',data)
def eee(request):
    updates=Updates.objects.filter(department='eee').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'eee.html',data)
def ece(request):
    updates=Updates.objects.filter(department='ece').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':updateslist}
    return render(request,'ece.html',data)
def pythonclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='python').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'pythonclub.html',data)
def codingclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='coding').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'codingclub.html',data)
def campus(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='campus').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'campusradio.html',data)
def ideaclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='idea').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'ideaclub.html',data)
def literacyclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='literacy').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'literacyclub.html',data)
def speakingclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='speaking').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'speakingclub.html',data)
def projectclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='project').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'projectclub.html',data)
def innerwheelclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='innerwheel').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'innerwheel.html',data)
def euphoriaclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='euphoria').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'euphoriaclub.html',data)
def graphicclub(request):
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updates'}
    updates=Updates.objects.filter(department='graphic').values()
    updateslist=[]
    for up in updates:
        updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
    data.update({'updates':updateslist})
    return render(request,'graphicclub.html',data)

def speechacc(request,id):
    if request.method=='POST':
        allpost=request.POST
        print(allpost)
        if allpost['text']=='open. pythonclub.' or allpost['text']=='open python.' or allpost['text']=='open python club.' :
            return HttpResponse('/pythonclub/'+id)
        elif allpost['text']=='open. graphicclub.' or allpost['text']=='open graphics.' or allpost['text']=='open graphics club.' :
            return HttpResponse('/graphicclub/'+id)
        elif allpost['text']=='open. projectclub.' or allpost['text']=='open project.' or allpost['text']=='open project club.' :
            return HttpResponse('/projectclub/'+id)
        elif allpost['text']=='open. euphoriaclub.' or allpost['text']=='open euphoria.' or allpost['text']=='open euphoria club.' :
            return HttpResponse('/euphoriaclub/'+id)
        elif allpost['text']=='open. innerwheelclub.' or allpost['text']=='open. innerwheel.' or allpost['text']=='open inner wheel club.' :
           return HttpResponse('/innerwheelclub/'+id)
        elif allpost['text']=='open. ideaclub.' or allpost['text']=='open idea.' or allpost['text']=='open idea club.' :
            return HttpResponse('/ideaclub/'+id)
        elif allpost['text']=='open. speakingclub.' or allpost['text']=='open. speaking.' or allpost['text']=='open speaking club.' :
            return HttpResponse('/speakingclub/'+id)
        elif allpost['text']=='open. codingclub.' or allpost['text']=='open. coding.' or allpost['text']=='open coding club.' :
            return HttpResponse('/codingclub/'+id)
        elif allpost['text']=='open. campusradioclub.' or allpost['text']=='open campus radio.' or allpost['text']=='open campusradio club.' :
            return HttpResponse('/campus/'+id)
        elif allpost['text']=='open. literacyclub.' or allpost['text']=='open. literacy.' or allpost['text']=='open literacy club.' :
            return HttpResponse('/literacyclub/'+id)
        elif allpost['text']=='open datascience.' or allpost['text']=='open ds.' or allpost['text']=='open data science.' :
            return HttpResponse('/datascience/'+id)
        elif allpost['text']=='open artifitialintiligence.' or allpost['text']=='open ai.' or allpost['text']=='open artificial intelligence.' :
            return HttpResponse('/cai/'+id)
        elif allpost['text']=='open ece.' or allpost['text']=='open. easy.' or allpost['text']=='open. ece.' :
            return HttpResponse('/ece/'+id)
        elif allpost['text']=='open eee.' or allpost['text']=='open. eee.' or allpost['text']=='open triple e.' :
            return HttpResponse('/eee/'+id)
        elif allpost['text']=='open ce.' or allpost['text']=='open. ce.' or allpost['text']=='open. ce.' :
            return HttpResponse('/ce/'+id)
        elif allpost['text']=='open cs.' or allpost['text']=='open. cs.' or allpost['text']=='open. cs.' :
            return HttpResponse('/cs/'+id)
        elif allpost['text']=='open mech.' or allpost['text']=='open. mech.' or allpost['text']=='open. mech.' :
            return HttpResponse('/mech/'+id)
        elif allpost['text']=='open mba.' or allpost['text']=='open. mba.' or allpost['text']=='open. mba.' :
            return HttpResponse('/mba/'+id)
        elif allpost['text']=='open mca.' or allpost['text']=='open. mca.' or allpost['text']=='open. mca.' :
            return HttpResponse('/mca/'+id)
        elif allpost['text']=='open cse.' or allpost['text']=='open. cse.' or allpost['text']=='open. cse.' :
            return HttpResponse('/cse/'+id)
        elif allpost['text']=='open home.' or allpost['text']=='back to home.' or allpost['text']=='back home.' :
            return HttpResponse('/account/'+id)
        elif allpost['text']=='open departments.' or allpost['text']=='open. departments.' or allpost['text']=='open departments.' :
            return HttpResponse('/departments'/+id)
        elif allpost['text']=='open clubs.' or allpost['text']=='open. clubs.' or allpost['text']=='open clubs.' :
            return HttpResponse('/clubs/'+id)
        elif allpost['text']=='open about.' or allpost['text']=='open. about.' or allpost['text']=='open about.' :
            return HttpResponse('/about/'+id)
        elif allpost['text']=='open logout.' or allpost['text']=='open. logout.' or allpost['text']=='open log out.' :
            return HttpResponse('/logout')
        elif allpost['text']=='open placement and training.' or allpost['text']=='open placement. and training.' or allpost['text']=='open. placement. and. training.' :
            return HttpResponse('/trainingandplacement/'+id)
def departmentsacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','rollno')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        return render(request,'departments.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        return render(request,'departments.html',data)
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'departments.html',data)
def clubsacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','rollno')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        return render(request,'clubs.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        return render(request,'clubs.html',data)
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'clubs.html',data)
def aboutacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','rollno')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        return render(request,'about.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        return render(request,'about.html',data)
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login']}
    return render(request,'about.html',data)
def profile(request,id): 
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','cover_pic','rollno','email','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'cover_pic':acc[0][3],
          'rollno':acc[0][4],'email':acc[0][5],'department':acc[0][6],'para':'/'+id,'para1':'account/'+id}
        quiz=Quizresult.objects.filter(idd=ObjectId(id)).values()
        quizdata=[]
        for quizs in quiz:
            quizdata.append({'date':quizs['date'],'title':quizs['title'],'score':quizs['score']})
        data.update({'quiz':quizdata,'total':len(quizdata)})
        return render(request,'profile.html',data)
    except:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','cover_pic','rollno','email','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'cover_pic':acc[0][3],
          'rollno':acc[0][4],'email':acc[0][5],'department':acc[0][6],'para':'/'+id,'para1':'account/'+id}
        try:
            updatedata=[]
            if acc[0][7]=='admin':
                update=Updates.objects.all().values()
                for updatee in update:
                    if updatee['url']=='/quiz':
                        updatedata.append({'date':updatee['date'],'title':updatee['urltext'],'url':updatee['url']+'/'+updatee['urltext']})
                    else:
                        updatedata.append({'date':updatee['date'],'title':updatee['urltext'],'url':updatee['url']})
                data.update({'updates':updatedata,'total':len(updatedata)})
            else:
                update=Updates.objects.filter(department=acc[0][7]).values()
                for updatee in update:
                    if updatee['url']=='/quiz':
                        updatedata.append({'date':updatee['date'],'title':updatee['urltext'],'url':updatee['url']+'/'+updatee['urltext']})
                    else:
                        updatedata.append({'date':updatee['date'],'title':updatee['urltext'],'url':updatee['url']})
                data.update({'updates':updatedata,'total':len(updatedata)})
            return render(request,'profileadmin.html',data)
        except:
            pass
    return render(request,'profile.html',data)
def profileview(request,id,id1):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','cover_pic','rollno','email','department')
        acct=StudentAccounts.objects.filter(_id=ObjectId(id1)).values_list('firstname','lastname','profile_img','cover_pic','rollno','email','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'viewname':acct[0][0]+acct[0][1],'viewcover_pic':acct[0][3],'viewprofile_img':acct[0][2],
          'viewrollno':acct[0][4],'viewemail':acct[0][5],'viewdepartment':acct[0][6],'para':'/'+id,'para1':'account/'+id}
        quiz=Quizresult.objects.filter(idd=ObjectId(id1)).values()
        quizdata=[]
        for quizs in quiz:
            quizdata.append({'date':quizs['date'],'title':quizs['title'],'score':quizs['score']})
        data.update({'quiz':quizdata})
    except:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','cover_pic','rollno','email','department')
        acct=StudentAccounts.objects.filter(_id=ObjectId(id1)).values_list('firstname','lastname','profile_img','cover_pic','rollno','email','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'viewname':acct[0][0]+acct[0][1],'viewcover_pic':acct[0][3],'viewprofile_img':acct[0][2],
          'viewrollno':acct[0][4],'viewemail':acct[0][5],'viewdepartment':acct[0][6],'para':'/'+id,'para1':'account/'+id}
        quiz=Quizresult.objects.filter(idd=ObjectId(id1)).values()
        quizdata=[]
        for quizs in quiz:
            quizdata.append({'date':quizs['date'],'title':quizs['title'],'score':quizs['score']})
        data.update({'quiz':quizdata,'total':len(quizdata)})
    return render(request,'profileview.html',data)
def datascienceacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Data Science':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
            'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='ds').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'datascience.html',data)

    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='ds').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='ds' :
            return render(request,'datascienceadmin.html',data)
        else:
            return render(request,'datascience.html',data) 
    except:
        pass
    
    return render(request,'datascience.html',data)
def cseacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Computer Science and Engineering':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
            'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='cse').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'cse.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='cse').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='cse' :
            return render(request,'cseadmin.html',data)
        else:
            return render(request,'cse.html',data) 
    except:
        pass
    return render(request,'cse.html',data)
def caiacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Artificial Intelligence':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
            'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='cai').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'cai.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='cai').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='cai' :
            return render(request,'caiadmin.html',data)
        else:
            return render(request,'cai.html',data) 
    except:
        pass
    return render(request,'cai.html',data)
def csacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Cyber Security':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='cs').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'cs.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='cs').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='cs' :
            return render(request,'csadmin.html',data)
        else:
            return render(request,'cai.html',data) 
    except:
        pass
    return render(request,'cai.html',data)
def ceacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Civil Engineering':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='ce').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'ce.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='ce').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='ce' :
            return render(request,'ceadmin.html',data)
        else:
            return render(request,'ce.html',data) 
    except:
        pass
def mechacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Mechanical Engineering':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='mech').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'mech.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='mech').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='mech' :
            return render(request,'mechadmin.html',data)
        else:
            return render(request,'mech.html',data) 
    except:
        pass
    return render(request,'mech.html',data)
def mbaacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Master of Business Administration':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='mba').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'mba.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='mba').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='mba' :
            return render(request,'mbaadmin.html',data)
        else:
            return render(request,'mba.html',data) 
    except:
        pass
    return render(request,'mba.html',data)
def mcaacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Master of Computer Applications':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='mca').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'mca.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='mca').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='mca' :
            return render(request,'mcaadmin.html',data)
        else:
            return render(request,'mca.html',data) 
    except:
        pass
    return render(request,'mca.html',data)
def eeeacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Electrical and Electronics Engineering':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='eee').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'eee.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='eee').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='eee' :
            return render(request,'eeeadmin.html',data)
        else:
            return render(request,'eee.html',data) 
    except:
        pass
    return render(request,'eee.html',data)
def eceacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email')
        if acc[0][3]=='Electronics and Communications Engineering':
            emails,accounts=allaccount(acc[0][3],id)
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'email':acc[0][4],'emaillist':emails,
              'acclist':accounts,'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        else:
            data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='ece').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        return render(request,'ece.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','email','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        updates=Updates.objects.filter(department='ece').values()
        updateslist=[]
        for up in updates:
            updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
        data.update({'updates':updateslist})
        if acc[0][5]=='admin' or acc[0][5]=='ece' :
            return render(request,'eceadmin.html',data)
        else:
            return render(request,'ece.html',data) 
    except:
        pass
    return render(request,'ece.html',data)
def trainAplacementacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='trainaplace').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('trainaplace',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='trainaplace').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'training&placement.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('trainaplace',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='trainaplace').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='trainaplace':
            return render(request,'training&placementadmin.html',data)
        else:
            return render(request,'training&placement.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'training&placement.html',data)
def pythonclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='python').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('python',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='python').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'pythonclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('python',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='python').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='python':
            return render(request,'pythonclubadmin.html',data)
        else:
            return render(request,'pthonclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'pythonclub.html',data)
def codingclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='coding').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('coding',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='codeing').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'codingclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('coding',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='coding').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='coding':
            return render(request,'codingclubadmin.html',data)
        else:
            return render(request,'codingclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'codingclub.html',data)
def campusacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='campusradio').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('campusradio',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='campus').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'campusradio.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('campusradio',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='campus').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='campus':
            return render(request,'campusradioadmin.html',data)
        else:
            return render(request,'campusradio.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'campusradio.html',data)
def ideaclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='idea').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('idea',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='idea').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'ideaclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('idea',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='idea').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='idea':
            return render(request,'ideaclubadmin.html',data)
        else:
            return render(request,'ideaclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'ideaclub.html',data)
def literacyclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='literacy').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('literacy',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='literacy').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'literacyclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('literacy',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='literacy').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='literacy':
            return render(request,'literacyclubadmin.html',data)
        else:
            return render(request,'literacyclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'literacyclub.html',data)
def speakingclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='speaking').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('speaking',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='speaking').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'speakingclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('speaking',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='speaking').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='speaking':
            return render(request,'speakingclubadmin.html',data)
        else:
            return render(request,'speakingclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'speakingclub.html',data)
def projectclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='project').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('project',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='project').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'projectclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('project',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='project').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='project':
            return render(request,'projectclubadmin.html',data)
        else:
            return render(request,'projectclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'projectclub.html',data)
def innerwheelclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='innerwheel').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('innerwheel',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='innerwheel').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'innerwheel.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('innerwheel',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='innerwheel').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass

        if acc[0][4]=='admin' or acc[0][4]=='innerwheel':

            return render(request,'innerwheelclubadmin.html',data)
        else:
            return render(request,'innerwheel.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'innerwheel.html',data)
def euphoriaclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='euphoria').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('euphoria',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='euphoria').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'euphoriaclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('euphoria',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='euphoria').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='euphoria':
            return render(request,'euphoriaclubadmin.html',data)
        else:
            return render(request,'euphoriaclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'euphoriaclub.html',data)
def graphicclubacc(request,id):
    try:
        acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id,'emaillist':[],'email':id}
        try: 
            emaillist=[]
            clubidemail=ClubsAccounts.objects.filter(club='graphic').values_list('studentobjectid')
            for ids in clubidemail:
                emaillist.append(ids[0])
            acclist=clubsaccount('graphic',id)
            data.update({'emaillist':emaillist,'acclist':acclist})
            updates=Updates.objects.filter(department='graphic').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        return render(request,'graphicclub.html',data)
    except:
        pass
    try:
        acc=AdminAccounts.objects.filter(_id=ObjectId(id)).values_list('firstname','lastname','profile_img','department','admin')
        data={'name':acc[0][0]+acc[0][1],'profile_img':acc[0][2],'log':['logout','Logout'],'para':'/'+id,'para1':'account/'+id}
        try: 
            acclist=clubsaccount('graphic',id)
            data.update({'acclist':acclist})
            updates=Updates.objects.filter(department='graphic').values()
            updateslist=[]
            for up in updates:
                updateslist.append({'date':up['date'],'urltext':up['urltext'],'url':up['url']})
            data.update({'updates':updateslist})
        except:
            pass
        if acc[0][4]=='admin' or acc[0][4]=='graphic':
            return render(request,'graphicclubadmin.html',data)
        else:
            return render(request,'graphicclub.html')
    except:
        pass
    data={'name':'GATES','profile_img':'/static/clg logo.jpg','log':['login','Login'],'updates':'updateslist'}
    return render(request,'graphicclub.html',data)

def postupdate(request,dp,id):
    if request.method=='POST':
        allpost=request.POST
        update=Updates()
        update.department=dp
        update.date=allpost['date']
        update.urltext=allpost['urltext']
        update.url=allpost['url']
        update.save()
        try:
            allposts=request.FILES
            if allposts['file']!='':
                fs.put(allposts['file'],filename=allpost['urltext'])
        except:
            pass
        return HttpResponse('done')   
def clubregistration(request,cb,id):
    if request.method=="POST":
        try:
            acc=StudentAccounts.objects.filter(_id=ObjectId(id)).values_list('email')
            club=ClubsAccounts()
            club.studentobjectid=id
            club.email=acc[0][0]
            club.club=cb
            club.save()
            print('successfully '+cb+' registered')
        except:
            pass
        return HttpResponse('nsiji')
def profilepic(request,id):
    if request.method=='POST':
        file=request.FILES
        try:
            stu=StudentAccounts.objects.filter(_id=ObjectId(id) )
            stu.update(profile_img='/image/profile_'+id+'.jpg')
        except:
            pass
        try:
            admin=AdminAccounts.objects.filter(_id=ObjectId(id) )
            admin.update(profile_img='/image/profile_'+id+'.jpg')
        except:
            pass
        try:
            idddd=db.fs.files.find({'filename':'profile_'+id+'.jpg'})
            for i in idddd:
                fsid=i['_id']
                fs.delete(fsid)
        except:
            pass
        fs.put(file['file'],filename='profile_'+id+'.jpg')
        
        return HttpResponse('hi')
def coverpic(request,id):
    if request.method=='POST':
        file=request.FILES
        try:
            stu=StudentAccounts.objects.filter(_id=ObjectId(id) )
            stu.update(cover_pic='/image/cover_'+id+'.jpg')
        except:
            pass
        try:
            admin=AdminAccounts.objects.filter(_id=ObjectId(id) )
            admin.update(cover_pic='/image/cover_'+id+'.jpg')
        except:
            pass
        try:
            idddd=db.fs.files.find({'filename':'cover_'+id+'.jpg'})
            for i in idddd:
                fsid=i['_id']
                fs.delete(fsid)
        except:
            pass
        fs.put(file['file'],filename='cover_'+id+'.jpg')
        
        return HttpResponse('hi')
def updates(request,title):
    data={'img':'/image/'+title,'title':title}
    return render(request,'updates.html',data)
def quizpost(request,cb,id):
    if request.method=='POST':
        allpost=request.POST
        quiz=Quiz()
        quiz.date=allpost['date']
        quiz.title=allpost['quiztitle']
        quiz.club=cb
        quiz.quiz={'question':[allpost['one'],allpost['two'],allpost['three'],allpost['four'],allpost['five'],allpost['six'],allpost['seven'],allpost['eight'],allpost['nine'],allpost['ten']],
                   'optionA':[allpost['oneA'],allpost['twoA'],allpost['threeA'],allpost['fourA'],allpost['fiveA'],allpost['sixA'],allpost['sevenA'],allpost['eightA'],allpost['nineA'],allpost['tenA']],
                   'optionB':[allpost['oneB'],allpost['twoB'],allpost['threeB'],allpost['fourB'],allpost['fiveB'],allpost['sixB'],allpost['sevenB'],allpost['eightB'],allpost['nineB'],allpost['tenB']],
                   'optionC':[allpost['oneC'],allpost['twoC'],allpost['threeC'],allpost['fourC'],allpost['fiveC'],allpost['sixC'],allpost['sevenC'],allpost['eightC'],allpost['nineC'],allpost['tenC']],
                   'optionD':[allpost['oneD'],allpost['twoD'],allpost['threeD'],allpost['fourD'],allpost['fiveD'],allpost['sixD'],allpost['sevenD'],allpost['eightD'],allpost['nineD'],allpost['tenD']],
                    'answer':[allpost['oneanswer'],allpost['twoanswer'],allpost['threeanswer'],allpost['fouranswer'],allpost['fiveanswer'],allpost['sixanswer'],allpost['sevenanswer'],allpost['eightanswer'],allpost['nineanswer'],allpost['tenanswer']]}
        quiz.save()
        quiz=Updates()
        quiz.department=cb
        quiz.date=allpost['date']
        quiz.urltext=allpost['quiztitle']
        quiz.url='/quiz'
        quiz.save()
        return HttpResponse('done')   
def quiz(request,id,title): 
    if request.method=='POST':
        quiz=Quiz.objects.filter(title=title).values()
        quizresult=Quizresult()
        quizresult.date=quiz[0]['date']
        quizresult.idd=id
        quizresult.title=title
        quizresult.quizresult={'answers':request.POST['answers']}
        quizresult.score=request.POST['score']
        quizresult.save()
        return HttpResponse('done')
    if request.method=='GET':
        try:
            quizresult=Quizresult.objects.filter(title=title,idd=id).values()
            
            if quizresult[0]['idd']==id:
                return HttpResponse('this quiz already complated')
            else:
                quiz=Quiz.objects.filter(title=title).values()
                data={'quiz':quiz[0]['quiz'],'title':title,'para':'/'+id}
                return render(request,'quiz.html',data)
        except:
            pass  
        quiz=Quiz.objects.filter(title=title).values()
        data={'quiz':quiz[0]['quiz'],'title':title,'para':'/'+id}
        return render(request,'quiz.html',data)
def quizz(requst,title):
    return  HttpResponseRedirect('/login')
def quizresult(request,id,title):
    if request.method=='GET':
        quizresult=Quizresult.objects.filter(idd=id,title=title).values()
        answer=quizresult[0]['quizresult']['answers'].split(',')
        quiz=Quiz.objects.filter(title=title).values()
        data={'quiz':quiz[0]['quiz'],'title':title,'para':'/'+id,'answer':answer}
        return render(request,'quizresult.html',data)
class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize
    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()
    def __iter__(self):
        return self
    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data  
def image(request,para):
    
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I) # type: ignore
    path=para
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    a=fs.find_one({'filename': path})
    size = a.length # type: ignore
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(fs.find_one({'filename': path}), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(fs.find_one({'filename': path})), content_type=content_type) # type: ignore
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp     