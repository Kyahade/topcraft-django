from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Worker, InventoryItem, Order, Project, UserProfile, CustomRequest, StandardProduct
from .forms import InventoryItemForm, WorkerForm, OrderForm, ProjectForm, CustomRequestForm, StandardProductForm

def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            try:
                profile = UserProfile.objects.get(user=request.user)

                if profile.role != role:
                    return HttpResponseForbidden("Access Denied")

            except UserProfile.DoesNotExist:
                return HttpResponseForbidden("No role assigned")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

@role_required('admin')
def dashboard(request):
    workers = Worker.objects.count()
    inventory = InventoryItem.objects.count()
    orders = Order.objects.count()
    projects = Project.objects.count()

    context = {
        'workers': workers,
        'inventory': inventory,
        'orders': orders,
        'projects': projects,
    }

    return render(request, 'admin/dashboard.html', context)

@role_required('admin')
def inventory(request):
    items = InventoryItem.objects.all()
    return render(request, 'admin/inventory.html', {'items': items})

@role_required('admin')
def workers(request):
    workers = Worker.objects.all()
    return render(request, 'admin/workers.html', {'workers': workers})

@role_required('admin')
def orders(request):
    orders = Order.objects.all()
    return render(request, 'admin/orders.html', {'orders': orders})

@role_required('admin')
def projects(request):
    projects = Project.objects.all()
    return render(request, 'admin/projects.html', {'projects': projects})

@role_required('admin')
def add_inventory(request):
    form = InventoryItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('inventory')

    return render(request, 'admin/inventory_form.html', {'form': form, 'title': 'Add Inventory Item'})

@role_required('admin')
def edit_inventory(request, id):
    item = get_object_or_404(InventoryItem, id=id)
    form = InventoryItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('inventory')

    return render(request, 'admin/inventory_form.html', {'form': form, 'title': 'Edit Inventory Item'})

@role_required('admin')
def delete_inventory(request, id):
    item = get_object_or_404(InventoryItem, id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('inventory')

    return render(request, 'admin/delete_confirm.html', {'item': item, 'type': 'Inventory Item'})

@role_required('admin')
def add_worker(request):
    form = WorkerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('workers')

    return render(request, 'admin/worker_form.html', {'form': form, 'title': 'Add Worker'})

@role_required('admin')
def edit_worker(request, id):
    worker = get_object_or_404(Worker, id=id)
    form = WorkerForm(request.POST or None, instance=worker)

    if form.is_valid():
        form.save()
        return redirect('workers')

    return render(request, 'admin/worker_form.html', {'form': form, 'title': 'Edit Worker'})

@role_required('admin')
def delete_worker(request, id):
    worker = get_object_or_404(Worker, id=id)

    if request.method == 'POST':
        worker.delete()
        return redirect('workers')

    return render(request, 'admin/delete_worker.html', {'worker': worker})

@role_required('admin')
def add_order(request):
    form = OrderForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orders')

    return render(request, 'admin/order_form.html', {'form': form, 'title': 'Add Order'})

@role_required('admin')
def edit_order(request, id):
    order = get_object_or_404(Order, id=id)
    form = OrderForm(request.POST or None, instance=order)

    if form.is_valid():
        form.save()
        return redirect('orders')

    return render(request, 'admin/order_form.html', {'form': form, 'title': 'Edit Order'})

@role_required('admin')
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        order.delete()
        return redirect('orders')

    return render(request, 'admin/delete_order.html', {'order': order})

@role_required('admin')
def add_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'admin/project_form.html', {'form': form, 'title': 'Add Project'})

@role_required('admin')
def edit_project(request, id):
    project = get_object_or_404(Project, id=id)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'admin/project_form.html', {'form': form, 'title': 'Edit Project'})

@role_required('admin')
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    return render(request, 'admin/delete_project.html', {'project': project})


def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                profile = UserProfile.objects.get(user=user)

                if profile.role == "admin":
                    return redirect("dashboard")
                elif profile.role == "customer":
                    return redirect("customer_dashboard")
                elif profile.role == "worker":
                    return redirect("worker_dashboard")

            except UserProfile.DoesNotExist:
                error = "No role assigned to this account."

        else:
            error = "Invalid username or password."

    return render(request, "core/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


@role_required('customer')
def customer_dashboard(request):
    return render(request, "customer/customer_dashboard.html")


@role_required('worker')
def worker_dashboard(request):
    return render(request, "worker/worker_dashboard.html")

@role_required('admin')
def custom_requests(request):
    requests = CustomRequest.objects.all()
    return render(request, 'admin/custom_requests.html', {'requests': requests})


@role_required('customer')
def add_custom_request(request):
    form = CustomRequestForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('customer_dashboard')

    return render(request, 'customer/custom_request_form.html', {'form': form, 'title': 'Submit Custom Request'})


@role_required('admin')
def edit_custom_request(request, id):
    custom_request = get_object_or_404(CustomRequest, id=id)
    form = CustomRequestForm(request.POST or None, instance=custom_request)

    if form.is_valid():
        form.save()
        return redirect('custom_requests')

    return render(request, 'admin/custom_request_form.html', {'form': form, 'title': 'Update Custom Request'})


@role_required('admin')
def delete_custom_request(request, id):
    custom_request = get_object_or_404(CustomRequest, id=id)

    if request.method == 'POST':
        custom_request.delete()
        return redirect('custom_requests')

    return render(request, 'admin/delete_custom_request.html', {'custom_request': custom_request})

@role_required('admin')
def standard_products(request):
    products = StandardProduct.objects.all()
    return render(request, 'admin/standard_products.html', {'products': products})


@role_required('admin')
def add_standard_product(request):
    form = StandardProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('standard_products')

    return render(request, 'admin/standard_product_form.html', {
        'form': form,
        'title': 'Add Standard Product'
    })


@role_required('admin')
def edit_standard_product(request, id):
    product = get_object_or_404(StandardProduct, id=id)
    form = StandardProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('standard_products')

    return render(request, 'admin/standard_product_form.html', {
        'form': form,
        'title': 'Edit Standard Product'
    })


@role_required('admin')
def delete_standard_product(request, id):
    product = get_object_or_404(StandardProduct, id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('standard_products')

    return render(request, 'admin/delete_standard_product.html', {
        'product': product
    })

