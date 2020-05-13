from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^add_book$', views.add_book),
    url(r'^books/(?P<id>\d+)$', views.show_book),
    url(r'^books/(?P<id>\d+)/edit$', views.edit_book),
    url(r'^books/(?P<id>\d+)/favorite$', views.favorite),
    url(r'^books/(?P<id>\d+)/unfavorite$', views.unfavorite),
    url(r'^books/(?P<id>\d+)/delete$', views.delete_book),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout)
]