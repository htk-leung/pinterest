from django.urls import path
from . import views	

urlpatterns = [
	path('', views.home, name="home"),
	path('onepin/<str:pinid>/', views.onepin, name="onepin"),
	path('allpins', views.allpins, name="allpins"),
	path('streampins/<str:stream_id>/', views.streampins, name="streampins"),
	path('boardpins/<str:board_id>/', views.boardpins, name="boardpins"),
	path('newpin', views.newpin, name="newpin"),
	path('newboard', views.newboard, name="newboard"),
	path('newstream', views.newstream, name="newstream"),
	path('myaccount/', views.myaccount, name="myaccount"),
	path('uaccount/<str:uid>/', views.uaccount, name="uaccount"),
	path('login/', views.login_user, name="login_user"),
	path('register/', views.register_user, name="register_user"),
	path('logout/', views.logout_user, name="logout_user"),
	path('settings', views.settings, name="settings"),
	path('savepintoboard/<str:pinid>/', views.savepintoboard, name="savepintoboard"),
	path('likepin/<str:pinid>/', views.likepin, name="likepin"),
	path('saveboardtostream', views.saveboardtostream, name="saveboardtostream"),
	path('addfriend/<str:uid>/', views.addfriend, name="addfriend"),
]