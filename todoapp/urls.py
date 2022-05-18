from django.urls import path
from . import views
app_name='todoapp'
urlpatterns = [
    path('', views.add,name='add'),
    path('delete/<int:id>', views.delete,name='delete'),
    path('update/<int:id>', views.update,name='update'),
    path('cbvhome/', views.TodoListView.as_view(),name='cbvhome'),
    path('cbvdetail/<int:pk>', views.TodoDetailView.as_view(),name='cbvdetail'),
    path('cbvupdate/<int:pk>', views.TodoUpdateView.as_view(),name='cbvupdate'),
    path('cbvdelete/<int:pk>', views.TodoDeleteView.as_view(),name='cbvdelete'),
]