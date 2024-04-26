from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.loginn,name="login"),
    path("awarness/",views.awarness,name="awarness"),
    path("logout/",views.signout,name="logout"),
    path("userhome/",views.userhome,name="userhome"),
    path("complain/",views.complains,name="complain"),
    path("preview/",views.preview,name="preview"),
    path("update/<id>",views.updateData,name="updateData"),
    path("delete/<id>",views.deleteData,name="deleteData")
]


