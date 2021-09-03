from django.urls import path

from admins.views import index,UserListView,UserUpdateView,UserCreateView,UserDeleteView,ProductCategoryCreateView,CategoriesListView,ProductCategoryUpdateView,CategoryDeleteView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users/create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users/remove/<int:pk>/', UserDeleteView.as_view(), name='admin_users_remove'),

    path('categories/create/', ProductCategoryCreateView.as_view(), name='category_create'),
    path('users/categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
]