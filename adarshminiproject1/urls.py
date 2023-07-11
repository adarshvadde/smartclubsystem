"""adarshminiproject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adarshminiproject1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('signin', views.signin),
    path('signsendemail', views.signsendemail),
    path('signinotpver', views.signinotpver),
    path('forget', views.forget),
    path('forgetsendemail', views.forgetsendemail),
    path('forgetotpver', views.forgetotpver),
    path('departments', views.departments),
    path('clubs', views.clubs),
    path('about', views.about),
    path('trainingandplacement', views.trainAplacement),
    path('speech', views.speech),
    path('speech/<id>', views.speechacc),


    path('datascience', views.datascience),
    path('cse', views.cse),
    path('cai', views.cai),
    path('cs', views.cs),
    path('ce', views.ce),
    path('ece', views.ece),
    path('eee', views.eee),
    path('mba', views.mba),
    path('mca', views.mca),
    path('mech', views.mech),
    path('pythonclub', views.pythonclub),
    path('codingclub', views.codingclub),
    path('campus', views.campus),
    path('ideaclub', views.ideaclub),
    path('literacyclub', views.literacyclub),
    path('speakingclub', views.speakingclub),
    path('projectclub', views.projectclub),
    path('innerwheelclub', views.innerwheelclub),
    path('euphoriaclub', views.euphoriaclub),
    path('graphicclub', views.graphicclub),
    
    path('account/<id>', views.account),
    path('departments/<id>', views.departmentsacc),
    path('clubs/<id>', views.clubsacc),
    path('about/<id>', views.aboutacc),
    path('profile', views.login),

    path('profile/<id>', views.profile),
    path('profileview/<id>/<id1>', views.profileview),
    
    path('datascience/<id>', views.datascienceacc),
    path('cse/<id>', views.cseacc),
    path('cai/<id>', views.caiacc),
    path('cs/<id>', views.csacc),
    path('ce/<id>', views.ceacc),
    path('ece/<id>', views.eceacc),
    path('eee/<id>', views.eeeacc),
    path('mba/<id>', views.mbaacc),
    path('mca/<id>', views.mcaacc),
    path('mech/<id>', views.mechacc),
    path('trainingandplacement/<id>', views.trainAplacementacc),
    path('pythonclub/<id>', views.pythonclubacc),
    path('codingclub/<id>', views.codingclubacc),
    path('campus/<id>', views.campusacc),
    path('ideaclub/<id>', views.ideaclubacc),
    path('literacyclub/<id>', views.literacyclubacc),
    path('speakingclub/<id>', views.speakingclubacc),
    path('projectclub/<id>', views.projectclubacc),
    path('innerwheelclub/<id>', views.innerwheelclubacc),
    path('euphoriaclub/<id>', views.euphoriaclubacc),
    path('graphicclub/<id>', views.graphicclubacc),
    
    
    path('postupdate/<dp>/<id>', views.postupdate),
    path('clubregistration/<cb>/<id>', views.clubregistration),
    path('profilepic/<id>', views.profilepic),
    path('coverpic/<id>', views.coverpic),
    path('updates/<title>', views.updates),
    path('quizpost/<cb>/<id>', views.quizpost),
    path('quiz/<id>/<title>', views.quiz),
    path('quiz/<title>', views.quizz),
    path('quizresult/<id>/<title>', views.quizresult),

    path('image/<para>', views.image),





    
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
