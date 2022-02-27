from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_registration',views.process_registration),
    path('process_login',views.process_login),
    path('logout',views.logout),
    path('summary',views.summary),
    path('addexpense',views.addexpense),
    path('process_expense',views.process_expense),
    path('expenses/<int:expense_id>',views.one_expense),
    path('delete/<int:expense_id>',views.delete),
    path('edit/<int:expense_id>',views.editexpense),
]