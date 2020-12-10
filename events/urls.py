from django.urls import path
from . import views

urlpatterns = [
    path('list', views.list_requested, name ='list'), #a query entered in search bar OR #ViewwAllEvents button was clicked
    path('post/', views.post_clicked, name ='post_events'),  #Post(+) button was clicked
    path('post/submit', views.post_clicked, name ='submit_post'),  #Submit button was clicked (after filling out the post)
    path('myevent',views.list_myevent,name = 'my_event'),
    path('', views.index, name='index'),
    path('addToEvent', views.addToEvent, name='addToEvent'),
    path('nearme', views.find_near_me, name='near_me'),
]
