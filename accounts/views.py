import asyncio
from datetime import datetime
import requests
import json
import uuid
from basicauth import encode
import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST
from notifications.signals import notify
from accounts.models import Account
from .mtnmomo import PayClass
from carts.models import *
from carts.views import _cart_id
from orders.models import Order, OrderProduct, PaymentRequest
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm, UserForm, UserProfileForm, AccountUpdateForm, VariationForm, ProductForm,  TestimonyForm
from .models import UserProfile, Testimony


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            customer_type = form.cleaned_data['customer_type']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                customer_type=customer_type,
            )
            user.phone_number = phone_number
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the product variations by cart id

                    product_variation = []

                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            # Set session expiry based on remember_me checkbox
            if remember_me:
                request.session.set_expiry(settings.SESSION_REMEMBER_ME_EXPIRY)
            else:
                # Use default session expiry
                request.session.set_expiry(0)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, "accounts/login.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
def manageUsers(request):
    users = Account.objects.all()
    context = {
        'users': users,
    }
    return render(request, "accounts/manageUsers.html", context)


def account_update(request, user_id):
    user = get_object_or_404(Account, pk=user_id)  # Fetch user by ID from URL
    if request.method == 'POST':
        account_form = AccountUpdateForm(request.POST, instance=user)
        if account_form.is_valid():
            account_form.save()
            update_session_auth_hash(request, user)  # Update session after password change (if applicable)
            messages.success(request, 'Account has been updated!')
            return redirect('account_update', user_id=user.id)  # Redirect back to update page for same user
    else:
        account_form = AccountUpdateForm(instance=user)
    context = {'account_form': account_form}
    return render(request, 'accounts/account_update.html', context)


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # RESETT PASSWORD EMAIL
            current_site = get_current_site(request)
            mail_subject = 'Reset Your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect("login")
        else:
            messages.error(request, 'Account does not exist! check the email you entered of create a new account.')
            return redirect("forgotpassword")
    return render(request, "accounts/forgotpassword.html")


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request, 'This link has expired')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    products = Product.objects.filter(seller=request.user, is_Available=True).order_by('id')
    seller = request.user
    seller_order_products = OrderProduct.objects.filter(product__seller=seller)
    paymentrequests = PaymentRequest.objects.none()
    for order_product in seller_order_products:
        total_cost = order_product.product_price * order_product.quantity
        if PaymentRequest.objects.filter(order_product=order_product).exists():
            pass
        else:
            payment_request = PaymentRequest.objects.create(
                order_product=order_product,
                product_name=order_product.product.product_name,
                order_number=order_product.order.order_number,
                quantity=order_product.quantity,
                total_cost=total_cost,
                seller=seller,
                phone_number=seller.phone_number,
                submitted_at=datetime.now()
            )

            payment_request.save()
        paymentrequests = PaymentRequest.objects.filter(seller=request.user).order_by('-submitted_at')

    context = {
        'orders': orders,
        "products": products,
        'paymentrequests': paymentrequests,

    }
    return render(request, 'accounts/my_orders.html', context)


@require_POST
def update_status_to_pending(request):
    recipients = Account.objects.filter(is_staff=True)
    order_product_id = request.POST.get('order_product_id')
    order_product = get_object_or_404(PaymentRequest, pk=order_product_id)
    order_product.status = "pending"
    order_product.save()
    user = request.user
    verb = f'{user.username} requested payment'
    for recipient in recipients:
        notify.send(user, recipient=recipient, verb=verb)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def inventory(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/inventory.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(pk=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('inventory')


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'You have successfully added a new product.')
            return redirect('add_product')
    else:
        form = ProductForm()

    return render(request, 'accounts/add_product.html', {'form': form})


def add_variation(request):
    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully added a new product variation.')
            return redirect('add_variation')
    else:
        form = VariationForm()

    return render(request, 'accounts/add_variation.html', {'form': form})


from .forms import ProductGalleryForm


def add_product_gallery(request):
    if request.method == 'POST':
        form = ProductGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.cleaned_data['product']
            for uploaded_file in form.cleaned_data['images']:
                ProductGallery.objects.create(product=product, image=uploaded_file)
            return redirect('add_product_gallery')
    else:
        form = ProductGalleryForm()

    return render(request, 'accounts/add_product_gallery.html', {'form': form})


def all_payment_request(request):
    payment_requests = PaymentRequest.objects.all().order_by('-submitted_at')
    context = {
        'payment_requests': payment_requests,
    }
    return render(request, 'accounts/payment_requests.html', context)


def make_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        payment_request_id = request.POST.get('payment_request_id')
        try:
            payment_request = PaymentRequest.objects.get(pk=payment_request_id)
            # Call the payment function here, passing payment_request attributes
            # For example:
            pay_instance = PayClass()
            response = pay_instance.withdrawmtnmomo(
                amount=payment_request.total_cost,
                currency="EUR",
                txt_ref=str(uuid.uuid4()),
                phone_number=phone_number,
                payermessage="Payment for order: " + payment_request.order_number
            )
            print(f"this is response3: {response['response']}")
            if response['response'] == 202:
                payment_request.status = 'paid'
                payment_request.save()
                messages.success(request, 'status: success, message: Payment initiated successfully')
                return redirect('all_payment_request')
            else:
                # Payment failed, handle accordingly
                messages.error(request, 'status: error, message: Payment failed')
                return redirect('all_payment_request')
        except PaymentRequest.DoesNotExist:
            messages.error(request, 'status: error, message: Payment request not found')
            return redirect('all_payment_request')




@login_required
def create_testimony(request):
  if request.method == 'POST':
    form = TestimonyForm(request.POST)
    if form.is_valid():
      testimony = form.save(commit=False)
      testimony.author = request.user
      testimony.save()
      return redirect('/')
  else:
    form = TestimonyForm()

  context = {'form': form}
  return render(request, 'accounts/create_testimony.html', context)



def aboutus(request):
    testimonies = Testimony.objects.filter(approved=True).order_by('-created_at')
    context = {
        'testimonies': testimonies,
    }
    return render(request, "aboutUs.html", context)

