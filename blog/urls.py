"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from users import views as user_views
app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
	path('',user_views.home, name="home"),
	path('signup/', user_views.signup, name="signup"),
	path('login/',user_views.login, name="login"),
	path('makepost/', user_views.create_posts, name="makepost"),
	path('error/',user_views.error, name="error"),
	path('success/', user_views.success,name="success"),
	path('dashboard/',user_views.dashboard, name="dashboard"),
	path('profile/', user_views.profile, name="profile"),
	path('logout/', user_views.logout, name="logout"),
    path('authenticate/',user_views.auth,name="auth"),
    path('test/',user_views.test,name="test"),
	path('posts/<int:post_id>',user_views.show_post, name="showpost"),
    path(r'^ajax/upvotepost/$', user_views.upvote_post, name='upvotepost'),
    path('resetpassword/<user_token>',user_views.change_password, name="changepassword"),
	path('<path:slug>', user_views.default, name="default"),
]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
         #url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
