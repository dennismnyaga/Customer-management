from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



def registerPage(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form':form}
    return render(request, 'CustApp/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            # return render(request, 'CustApp/login.html')
    context = {}
    return render(request, 'CustApp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers,'total_orders':total_orders, 'delivered':delivered,'pending':pending, 'total_customers':total_customers}
    return render(request, 'CustApp/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'CustApp/products.html', {'products':products})


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'CustApp/customer.html', context)



def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet( queryset=Order.objects.none() ,instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing Post', request.POST)
        # form = OrderForm(request.POST)
        formset = orderFormSet( request.POST ,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'CustApp/order_form.html', context)



def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing Post', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'CustApp/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {'item': order}
    return render(request, 'CustApp/delete.html', context)
