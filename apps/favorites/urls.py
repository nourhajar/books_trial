from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^congrats$', views.congrats),
    url(r'^book/(?P<id>\d+)$$', views.book),
    url(r'^add_book$', views.add_book),
    url(r'^remove_favorite/(?P<id>\d+)$', views.remove_favorite),
    url(r'^add_favorite/(?P<id>\d+)$', views.add_favorite),
    url(r'^register/process$', views.register),
    url(r'^login/process$', views.login),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^edit/update/(?P<id>\d+)$', views.update)
]