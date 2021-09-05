from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connection
from django.db.models import F

from products.models import ProductCategory
from users.forms import ShopUserProfileEdit
from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from admins.forms import ProductCategoryAdminEditForm


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'Админ-панель'}
    return render(request, 'admins/index.html', context)


# FBV for CBV
# @user_passes_test(lambda u: u.is_staff)
# def admin_users(request):
#     context = {'title': 'Админ-панель - Пользовтаели', 'users': User.objects.all()}
#     return render(request, 'admins/admin-users-read.html', context)


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['title'] = 'Админ-панель - Пользовтаели'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request)


#  @user_passes_test(lambda u: u.is_staff)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminRegistrationForm()
#     context = {'title': 'Админ-панель - Создание пользователя', 'form': form}
#     return render(request, 'admins/admin-users-create.html', context)
class UserCreateView(CreateView):
    model = User
    form_class = UserAdminRegistrationForm
    template_name = 'admins/admin-users-create.html'
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'Админ-панель -  Создание пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request)


# @user_passes_test(lambda u: u.is_staff)
# def admin_users_update(request, pk):
#     selected_user = User.objects.get(id=pk)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
#         # profile_form = ShopUserProfileEdit(request.POST, instance=request.user.userprofile)
#
#         if form.is_valid() :
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#         # profile_form = ShopUserProfileEdit(request.POST, instance=request.user.userprofile)
#     context = {
#         'title': 'Админ-панель - Редактирование пользовтаеля',
#         'form': form,
#         'selected_user': selected_user,
#         # 'profile_form':profile_form
#     }
#     return render(request, 'admins/admin-users-update-delete.html', context)
class UserUpdateView(UpdateView):
    model = User
    form_class = UserAdminProfileForm
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'Админ-панель -  Редактирование пользовтаеля'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request)


# @user_passes_test(lambda u: u.is_staff)
# def admin_users_remove(request, pk):
#     user = User.objects.get(id=pk)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admins:admin_users'))
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request)


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'admins/categories.html'
    # context_object_name = 'objects'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        context['title'] = 'Админ-панель - Пользовтаели'
        return context
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesListView, self).dispatch(request)
# def admin_users_categories(request):
#     context = {'title': 'Админ-панель - Категория', 'users': ProductCategory.objects.all()}
#     return render(request, 'admins/categories.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'admins/category_update.html'
    form_class = ProductCategoryAdminEditForm
    success_url = reverse_lazy('admin_staff:categories')



class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'admins/category_update.html'
    form_class = ProductCategoryAdminEditForm
    success_url = 'admins/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'

        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount}% к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'admins/category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # self.object.is_active=False
        # self.object.save()
        return HttpResponseRedirect(self.get_success_url())

