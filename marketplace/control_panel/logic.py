from .forms import CreateCategoryForm, RemoveCategoryForm, AddDeviceForm
from devices.models import Category, Review, Device
from django.shortcuts import get_object_or_404
from functools import wraps
from django.http import HttpResponseForbidden


def create_category(request):
    create_form = CreateCategoryForm()
    warning_message = None

    if request.method == "POST" and 'create_category' in request.POST:
        create_form = CreateCategoryForm(request.POST)
        if request.method == 'POST':
            if create_form.is_valid() and \
                    not Category.objects.filter(name=create_form.cleaned_data['name']).exists():
                create_form.save()
            else:
                warning_message = "Категория с таким названием уже существует. "

    return {'create_form': create_form, 'warning_message': warning_message}


def remove_category(request):
    remove_form = RemoveCategoryForm()
    if request.method == "POST":
        if 'remove_category' in request.POST:
            remove_category_form = RemoveCategoryForm(request.POST)

            if request.method == 'POST':
                if remove_category_form.is_valid():
                    category_name = remove_category_form.cleaned_data['name']
                    matching_categories = Category.objects.filter(name=category_name)

                    if matching_categories.exists():
                        category = matching_categories.first()
                        category.delete()
    return remove_form


def remove_review(request):
    if request.method == 'POST':
        review_id_to_delete = request.POST.get('delete_review_id')
        if review_id_to_delete:
            review_to_delete = get_object_or_404(Review, id=review_id_to_delete)
            review_to_delete.delete()


def add_device(request):
    if 'add_device' in request.POST:
        add_device_form = AddDeviceForm(request.POST, request.FILES)
        if add_device_form.is_valid():
            add_device_form.save()
    else:
        add_device_form = AddDeviceForm()
    return add_device_form


def has_rights(user, group_name):
    return user.groups.filter(name=group_name).exists()


def check_group(group_name=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if has_rights(request.user, group_name):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()

        return wrapped_view

    return decorator
