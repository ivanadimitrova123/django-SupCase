from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CheckoutForm, ItemForm


def cases(request):
    query = request.GET.get('search_query', '')
    phone_type = request.GET.getlist('phone_type')
    material = request.GET.getlist('material')
    color = request.GET.getlist('color')
    all_cases = Product.objects.all()

    if query:
        all_cases = all_cases.filter(phone_type__icontains=query)

    if phone_type:
        all_cases = all_cases.filter(phone_type__in=phone_type)

    if material:
        all_cases = all_cases.filter(material__in=material)

    if color:
        all_cases = all_cases.filter(color__in=color)

    return render(request, 'cases.html',
                  {'cases': all_cases, 'query': query, 'selected_phone_type': phone_type, 'selected_material': material,
                   'selected_color': color, 'user': request.user})


@login_required(login_url='login')
def case_details(request, case_id):
    case = get_object_or_404(Product, id=case_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        # Check if the purchased quantity is available
        if quantity <= case.quantity:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=case)
            cart_item.quantity = quantity
            cart_item.save()
            return redirect('cart_items')
        else:
            return HttpResponse("Insufficient quantity available")
    return render(request, 'case_details.html', {'case': case})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    item.delete()
    return redirect('cases')


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('case_details', case_id=item.id)
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_product.html', {'form': form, 'item': item})


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('case_details', case_id=form.save().id)  # Redirect to the cart or any other appropriate URL
    else:
        form = ItemForm()
    return render(request, 'add_product.html', {'form': form})


@login_required(login_url='login')
def cart_items(request):
    items = CartItem.objects.filter(cart__user=request.user)
    cart_total = sum(item.product.price * item.quantity for item in items)
    context = {'cart_items': items, 'total': cart_total}
    return render(request, 'cart_items.html', context)


@login_required
def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_items')


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.cart = request.user.cart  # Assuming you have associated each user with a cart
            order.total_amount = order.calculate_total_amount()  # Calculate the total amount
            order.save()
            # Subtract the purchased quantities from the products' quantities
            items = order.cart.items.all()
            for cart_item in items:
                cart_item.product.quantity -= cart_item.quantity
                cart_item.product.save()
            # Clear the cart items
            request.user.cart.items.all().delete()
            # Redirect or render success page
            return redirect('final_site')
        # else:
        #     return redirect('cases')
    else:
        form = CheckoutForm()
    context = {'form': form}
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def final_site(request):
    return render(request, 'final_site.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cases')
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    return render(request, 'login.html')


