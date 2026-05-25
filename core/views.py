from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Worker, InventoryItem, Order, Project, UserProfile, CustomRequest, StandardProduct
from .forms import InventoryItemForm, WorkerForm, OrderForm, ProjectForm, CustomRequestForm, StandardProductForm, AssignWorkerForm, CustomerProfileForm


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
    orders = Order.objects.count()
    projects = Project.objects.count()
    workers = Worker.objects.count()
    inventory = InventoryItem.objects.count()

    recent_orders = Order.objects.order_by('-created_at')[:5]
    low_stock_items = InventoryItem.objects.filter(quantity__lte=5)

    return render(request, 'admin_panel/dashboard.html', {
        'orders': orders,
        'projects': projects,
        'workers': workers,
        'inventory': inventory,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
    })
    
def assign_worker(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = AssignWorkerForm(request.POST, instance=project)

        if form.is_valid():
            form.save()

            if project.order:
                project.order.assigned_worker = project.assigned_worker
                project.order.status = 'assigned'
                project.order.save()

            project.status = 'Assigned'
            project.save()

            return redirect('projects')
    else:
        form = AssignWorkerForm(instance=project)

    return render(request, 'admin_panel/assign_worker.html', {
        'form': form,
        'project': project
    })

@role_required('admin')
def inventory(request):
    items = InventoryItem.objects.all()
    return render(request, 'admin_panel/inventory.html', {'items': items})

@role_required('admin')
def workers(request):
    workers = Worker.objects.all()
    return render(request, 'admin_panel/workers.html', {'workers': workers})

@role_required('admin')
def orders(request):
    orders = Order.objects.all()
    return render(request, 'admin_panel/orders.html', {'orders': orders})

@role_required('admin')
def projects(request):
    projects = Project.objects.all()
    return render(request, 'admin_panel/projects.html', {'projects': projects})

@role_required('admin')
def add_inventory(request):
    form = InventoryItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('inventory')

    return render(request, 'admin_panel/inventory_form.html', {'form': form, 'title': 'Add Inventory Item'})

@role_required('admin')
def edit_inventory(request, id):
    item = get_object_or_404(InventoryItem, id=id)
    form = InventoryItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('inventory')

    return render(request, 'admin_panel/inventory_form.html', {'form': form, 'title': 'Edit Inventory Item'})

@role_required('admin')
def delete_inventory(request, id):
    item = get_object_or_404(InventoryItem, id=id)

    if request.method == 'POST':
        item.delete()
        return redirect('inventory')

    return render(request, 'admin_panel/delete_confirm.html', {'item': item, 'type': 'Inventory Item'})

@role_required('admin')
def add_worker(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        role = request.POST.get('role')
        skill = request.POST.get('skill')
        status = request.POST.get('status')

        if User.objects.filter(username=username).exists():
            return render(request, 'admin_panel/worker_form.html', {
                'title': 'Add Worker',
                'error': 'Username already exists. Please use another username.'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role='worker'
        )

        Worker.objects.create(
            user=user,
            name=name,
            role=role,
            skill=skill,
            status=status
        )

        return redirect('workers')

    return render(request, 'admin_panel/worker_form.html', {
        'title': 'Add Worker'
    })

@role_required('admin')
def edit_worker(request, id):
    worker = get_object_or_404(Worker, id=id)
    form = WorkerForm(request.POST or None, instance=worker)

    if form.is_valid():
        form.save()
        return redirect('workers')

    return render(request, 'admin_panel/worker_form.html', {'form': form, 'title': 'Edit Worker'})

@role_required('admin')
def delete_worker(request, id):
    worker = get_object_or_404(Worker, id=id)

    if request.method == 'POST':
        worker.delete()
        return redirect('workers')

    return render(request, 'admin_panel/delete_worker.html', {'worker': worker})

@role_required('admin')
def add_order(request):
    form = OrderForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('orders')

    return render(request, 'admin_panel/order_form.html', {'form': form, 'title': 'Add Order'})

@role_required('admin')
def edit_order(request, id):
    order = get_object_or_404(Order, id=id)
    form = OrderForm(request.POST or None, instance=order)

    if form.is_valid():
        form.save()
        return redirect('orders')

    return render(request, 'admin_panel/order_form.html', {'form': form, 'title': 'Edit Order'})

@role_required('admin')
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        order.delete()
        return redirect('orders')

    return render(request, 'admin_panel/delete_order.html', {'order': order})

@role_required('admin')
def add_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'admin_panel/project_form.html', {'form': form, 'title': 'Add Project'})

@role_required('admin')
def edit_project(request, id):
    project = get_object_or_404(Project, id=id)
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'admin_panel/project_form.html', {'form': form, 'title': 'Edit Project'})

@role_required('admin')
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    return render(request, 'admin_panel/delete_project.html', {'project': project})


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
    worker = Worker.objects.filter(user=request.user).first()

    projects = Project.objects.filter(
        assigned_worker=worker
    ).exclude(status="Completed")

    return render(request, 'worker/worker_dashboard.html', {
        'projects': projects
    })

@role_required('admin')
def custom_requests(request):
    requests = CustomRequest.objects.all()
    return render(request, 'admin_panel/custom_requests.html', {'requests': requests})


@role_required('customer')
def add_custom_request(request):
    if request.method == "POST":
        form = CustomRequestForm(request.POST)

        if form.is_valid():
            custom_request = form.save()

            Order.objects.create(
                customer=request.user,
                order_type="custom",
                status="pending"
            )

            messages.success(request, "Custom request submitted successfully.")
            return redirect('customer_orders')

    else:
        form = CustomRequestForm()

    return render(request, 'customer/custom_request_form.html', {
        'form': form,
        'title': 'Submit Custom Request'
    })

@role_required('admin')
def edit_custom_request(request, id):
    custom_request = get_object_or_404(CustomRequest, id=id)
    form = CustomRequestForm(request.POST or None, instance=custom_request)

    if form.is_valid():
        form.save()
        return redirect('custom_requests')

    return render(request, 'admin_panel/custom_request_form.html', {'form': form, 'title': 'Update Custom Request'})


@role_required('admin')
def delete_custom_request(request, id):
    custom_request = get_object_or_404(CustomRequest, id=id)

    if request.method == 'POST':
        custom_request.delete()
        return redirect('custom_requests')

    return render(request, 'admin_panel/delete_custom_request.html', {'custom_request': custom_request})

@role_required('admin')
def standard_products(request):
    products = StandardProduct.objects.all()
    return render(request, 'admin_panel/standard_products.html', {'products': products})


@role_required('admin')
def add_standard_product(request):
    form = StandardProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('standard_products')

    return render(request, 'admin_panel/standard_product_form.html', {
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

    return render(request, 'admin_panel/standard_product_form.html', {
        'form': form,
        'title': 'Edit Standard Product'
    })


@role_required('admin')
def delete_standard_product(request, id):
    product = get_object_or_404(StandardProduct, id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('standard_products')

    return render(request, 'admin_panel/delete_standard_product.html', {
        'product': product
    })

@role_required('customer')
def customer_products(request):
    products = StandardProduct.objects.filter(status="Available")
    return render(request, 'customer/customer_products.html', {'products': products})


@role_required('customer')
def order_standard_product(request, product_id):
    product = get_object_or_404(StandardProduct, id=product_id)

    if request.method == "POST":
        Order.objects.create(
            customer=request.user,
            standard_product=product,
            order_type="standard",
            status="pending"
        )
        messages.success(request, "Order submitted successfully. Please wait for admin review.")
        return redirect('customer_orders')

    return render(request, 'customer/order_standard_product.html', {'product': product})


@role_required('customer')
def customer_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'customer/customer_orders.html', {'orders': orders})

@role_required('worker')
def start_project(request, pk):
    project = Project.objects.get(pk=pk)

    project.status = "In Production"
    project.save()

    return redirect('worker_dashboard')

@role_required('worker')
def complete_project(request, pk):
    project = Project.objects.get(pk=pk)

    project.status = "Completed"
    project.save()

    return redirect('worker_dashboard')

@role_required('worker')
def start_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'in_progress'
    order.save()

    return redirect('worker_dashboard')


@role_required('worker')
def complete_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = 'completed'
    order.save()

    return redirect('worker_dashboard')

def accept_order(request, pk):
    order = Order.objects.get(pk=pk)

    order.status = 'accepted'
    order.save()

    Project.objects.get_or_create(
        order=order,
        defaults={
            'project_name': f'Order #{order.id} Project',
            'assigned_worker': order.assigned_worker,
            'status': 'Assigned',
            'deadline': timezone.now().date(),
        }
    )

    return redirect('orders')


def reject_order(request, pk):
    order = Order.objects.get(pk=pk)

    order.status = 'rejected'
    order.save()

    return redirect('orders')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role="customer"
        )

        messages.success(request, "Customer account created successfully. Please login.")
        return redirect("login")

    return render(request, "core/register.html")

@login_required
def customer_profile(request):
    profile = request.user.userprofile

    if request.method == "POST":
        form = CustomerProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Profile updated successfully.")
            return redirect("customer_profile")

    else:
        form = CustomerProfileForm(
            instance=profile,
            user=request.user
        )

    return render(request, "customer/profile.html", {
        "form": form,
        "profile": profile
    })
