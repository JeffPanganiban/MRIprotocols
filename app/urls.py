
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('home', views.home),
    path('login', views.login),
    path('new_reg', views.new_reg),
    path('build', views.build),
    path('new_category', views.new_category),
    path('select_category', views.select_category),
    path('select_category/<str:category_name>', views.new_protocol),
    path('create_protocol', views.create_protocol),
    path('add_sequences/<int:id>', views.add_sequences),
    path('add_to_protocol', views.add_to_protocol),
    path('review/<int:id>', views.review),
    path('details/<int:id>', views.details),
    path('edit/<int:id>', views.edit),
    path('edit_sequence/<int:id>', views.edit_sequence),
    path('edit_sequence_submit', views.edit_sequence_submit),
    path('delete_sequence', views.delete_sequence),
    path('edit_to_protocol', views.edit_to_protocol),
    path('delete_protocol', views.delete_protocol),
    path('logout', views.logout),
]