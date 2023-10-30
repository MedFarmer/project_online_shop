from django.shortcuts import render, redirect
from .models import Product, Order, Stock, Textile, Color, Size, AdditionalImage, BoughtProduct
from .forms import AddProductForm, AddStockForm, LoginForm, UpdateForm, OrderForm, AddTextileForm, AddColorForm, AddSizeForm, AddImageForm, SignUpForm, BuyForm
from django.views.generic import ListView, CreateView, View, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Any
import json
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

"""index, catalague, detail pages"""

class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class Home(ListView):
    def get(self, request):
        catalague = Product.objects.all()
        # paginator = Paginator(data, 4)
        # if 'page' in request.GET:
        #     page_num = request.GET['page']
        # else:
        #     page_num = 1
        # page = paginator.get_page(page_num)
        context = {'catalague':catalague}    
        if request.user.is_authenticated:
            print('authenticated')
            try:
                if 'first_buy' in request.session:
                    print('first buy')
                    products_id = request.session['first_buy']['product']
                    color = request.session['first_buy']['color']
                    size = request.session['first_buy']['size']
                    order_quantity = request.session['first_buy']['quantity']
                    price = request.session['first_buy']['price']
                    subtotal = request.session['first_buy']['subtotal']
                    Order.objects.create(clients_id=request.user.id, products_id=products_id, color=color, size=size, order_quantity=order_quantity, price=price, subtotal=subtotal)
                    
                    product_query = Product.objects.get(pk=products_id)
                    quantity_to_delete = -order_quantity
                    color_query = Color.objects.get(color=color)                    
                    Stock.objects.create(product=product_query, color=color_query, size=size, quantity=quantity_to_delete)                  
                    
                    del request.session['first_buy']
                    return render(request, 'home.html', context)
                else:
                    return render(request, 'home.html', context)
            except Exception as e:
                return render(request, 'home.html', context)
        else:
            return render(request, 'home.html', context)

class Detail(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'products'
    # pk_url_kwarg = 'id'    
        
    def get_context_data(self, **kwargs):        
        sizes = ["XS","S","M","L","XL","2XL","3XL","4XL"]        
        size_list = []
        context = super().get_context_data(**kwargs)        
        product_id = self.object.id
        Size.objects.all().delete()
        Size.objects.create(size=product_id)
        selection_by_articule = Stock.objects.filter(product=product_id)
        colors = [each.color for each in selection_by_articule]
        unique_colors = list(set(colors))
        
        for color in unique_colors:
            size_dict = {}
            size_dict['color'] = color.color
            for size in sizes:
                filtered = Stock.objects.filter(product=self.object.id, color=color, size=size)
                total_quantity = sum(item.quantity for item in filtered)
                size_dict[size] = total_quantity
            size_list.append(size_dict)
        context['size_list'] = size_list
        context['colors'] = unique_colors
        
        additional_images = AdditionalImage.objects.filter(product=product_id)
        context['additional_images'] = additional_images        
        return context
        
    def post(self, request, pk):        
        form = OrderForm(request.POST)
        
        if form['color'] != '' and form['size'] != '' and form['order_quantity'] != '':
            if form.is_valid():            
                color = form.cleaned_data['color']
                size = form.cleaned_data['size']
                order_quantity = form.cleaned_data['order_quantity']
                products = pk                
                clients = request.user.id                
                product_query = Product.objects.get(pk=products)
                price = product_query.price
                subtotal = price * order_quantity
                
                if request.user.is_authenticated:
                    Order.objects.create(clients_id=clients, products_id=products, color=color, size=size, order_quantity=order_quantity, price=price, subtotal=subtotal)
                    quantity_to_delete = -order_quantity
                    color_query = Color.objects.get(color=color)                    
                    Stock.objects.create(product=product_query, color=color_query, size=size, quantity=quantity_to_delete)                    
                    return redirect('home')
                else:                
                    request.session['first_buy'] = {'product':products, 'color':color, 'size':size, 'quantity':order_quantity, 'price':price, 'subtotal':subtotal}
                    print('session is below product')
                    print(request.session['first_buy']['product'])
                    return redirect('login')                                
        else:
            context = {'form':form}
            return render(request, 'detail.html', context)

def get_available_sizes(request):
    all_sizes = ["XS","S","M","L","XL","2XL","3XL","4XL"]
    available_sizes = []
    selected_color = request.GET.get('color')
    if selected_color:
        product_ids = Size.objects.all().values_list('size', flat=True)
        product_id = int(product_ids[0])
        selected = Color.objects.filter(color = selected_color).values_list('id', flat=True)
        selected_color_id = int(selected[0])
        print(product_id)
        print(selected_color_id)
        filtered_by_color = Stock.objects.filter(product = product_id, color_id = selected_color_id)
        sizes = [each.size for each in filtered_by_color]
        available = list(set(sizes))
        for each in all_sizes:
            if each in available:
                available_sizes.append(each)
        print(available_sizes)
        return JsonResponse({'size': available_sizes, 'product_id': product_id, 'color_id': selected_color_id})
    else:
        return JsonResponse({'size': available_sizes})

def get_available_quantities(request):      
    selected_size = request.GET.get('size')
    if selected_size:
        response = get_available_sizes(request)
        data = json.loads(response.content.decode('utf-8'))
        product_id = data['product_id']
        color_id = data['color_id']
        filtered_by_size = Stock.objects.filter(product = product_id, color = color_id, size = selected_size)
        quantity = sum([each.quantity for each in filtered_by_size])
        quantity_to_select = [x for x in range(1, quantity + 1)]    
        print(quantity_to_select)        
        return JsonResponse({'quantity': quantity_to_select})
    else:
        return JsonResponse({'quantity': ''})

"""Adding, Deleting, Updating done by Admin side""" 

class AddProduct(View):     
    def get(self, request):
        form= AddProductForm()
        products = Product.objects.all().order_by('-id')        
        context = {'info': products, 'form': form}
        return render(request, 'addproduct.html', context)
    
    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            textile = form.cleaned_data['textile']
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            Product.objects.create(name = name, price = price, textile = textile, image = image, description = description)            
            
            return redirect('addproduct')
        else:
            return render(request, 'addproduct.html', {'form':form})

class Delete(DeleteView):
    model = Product
    template_name = 'confirmation.html'
    success_url = reverse_lazy('home')

class AddImage(CreateView):
    
    def post(self, request, product_pk):
        form = AddImageForm(request.POST, request.FILES)
        product = Product.objects.get(pk=product_pk)
        
        additional_images = AdditionalImage.objects.filter(product=product)
        if form.is_valid():
            additional_image = form.cleaned_data['additional_image']           
            AdditionalImage.objects.create(product=product, additional_image=additional_image)            
            messages.success(request, 'you added new image')
            context={'form':form, 'additional_images':additional_images}
            
            return render(request, 'addimage.html', context)
        else:
            messages.error(request, 'form is not valid')            
            context={'form':form, 'additional_images':additional_images}
            return render(request, 'addimage.html', context)
    
    def get(self, request, product_pk):
        product = Product.objects.get(pk=product_pk)  
        additional_images = AdditionalImage.objects.filter(product=product)
        context = {'additional_images':additional_images}
        return render(request, 'addimage.html', context)

class AddImageDelete(View):
    
    def get(self, request, product_pk, image_pk):        
        image_to_delete = AdditionalImage.objects.get(pk=image_pk)
        context = {'image_to_delete':image_to_delete}
        return render(request, 'addimage_delete.html', context)
    
    def post(self, request, product_pk, image_pk):
        AdditionalImage.objects.filter(pk=image_pk).delete()
        additional_images = AdditionalImage.objects.filter(product=product_pk)
        context = {'additional_images':additional_images}
        return render(request, 'addimage.html', context)    

class AddStock(View):
    def post(self, request):
        form = AddStockForm(request.POST)
        if form.is_valid():
            articule = form.cleaned_data['product']
            color = form.cleaned_data['color']
            size_xs = form.cleaned_data['size_xs']
            size_s = form.cleaned_data['size_s']
            size_m = form.cleaned_data['size_m']
            size_l = form.cleaned_data['size_l']
            size_xl = form.cleaned_data['size_xl']
            size_2xl = form.cleaned_data['size_2xl']
            size_3xl = form.cleaned_data['size_3xl']
            size_4xl = form.cleaned_data['size_4xl']
            all_sizes = {'XS':size_xs, 'S':size_s, 'M':size_m, 'L':size_l, 'XL':size_xl, '2XL':size_2xl, '3XL':size_3xl, '4XL':size_4xl}
            print(all_sizes)
            for key, value in all_sizes.items():
                if value > 0:
                    Stock.objects.create(product=articule, color=color, size = key, quantity = value)            
            return redirect('addstock')             
        else:
            return render(request, 'addstock.html', {'form':form})
    
    def get(self, request):
        form = AddStockForm()
        stock = Stock.objects.all().order_by('-id')
        context = {'form': form, 'stock':stock}
        return render(request, 'addstock.html', context)
    
class AddTextile(CreateView):
    model = Textile
    form_class = AddTextileForm
    template_name = 'addtextile.html'
    success_url = reverse_lazy('addtextile')    
        
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['textiles'] = Textile.objects.all()
        return context   

# class AddSize(CreateView):
#     model = Size
#     form_class = AddSizeForm
#     template_name = 'addsize.html'
#     success_url = reverse_lazy('addsize')
    
#     def get_context_data(self, **kwargs):        
#         context = super().get_context_data(**kwargs)
#         context['sizes'] = Size.objects.all()
#         return context

class AddColor(CreateView):
    model = Color
    form_class = AddColorForm
    template_name = 'addcolor.html'
    success_url = reverse_lazy('addcolor')
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        return context

class DeleteColorView(DeleteView):
    model = Color
    template_name = 'delete_color.html'
    success_url = reverse_lazy('home')

class Update(UpdateView):
    model = Product
    template_name = 'update.html'
    form_class = UpdateForm
    success_url = reverse_lazy('detail', kwargs={'pk': 'your_primary_key_value'})

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.pk})

""" User authorization, authentication classes """

class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    
    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'verify your email'
        message = f'Hello {user.username}, plase click the link below to verify your email :\n\n{verify_url}'        
        send_mail(subject, message, 'medet20231020@gmail.com', [user.username])
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        print(user.is_active)
        user.email = user.username
        user.save()
        self.send_verification_email(user)                
        return response              
    
class Login(LoginView):
    template_name = 'login.html'
    authetication_form = LoginForm
    next_page = 'home'

class Logout(LogoutView):
    next_page = 'home'

class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = User.objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verify_success')
        else:
            return redirect('verify_error')

class VerifySuccessView(View):
    def get(self, request):        
        return render(request, 'verify_success.html')

class VerifyErrorView(View):
    def get(self, request):        
        return render(request, 'verify_error.html')

class Users(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

class UsersDelete(DeleteView):
    model = User
    template_name = 'delete_users.html'
    success_url = reverse_lazy('users')

"""Order, basket, buy classes"""
from .signals import purchase_signal

class Basket(View):    
    def get(self, request, user_pk):
        total_value = 0
        basket = Order.objects.filter(clients = user_pk)
        total_value = sum([x.subtotal for x in basket])
        context = {'basket': basket, 'total':total_value}        
        return render(request, 'basket.html', context)
    
    def post(self, request, user_pk):
        basket = Order.objects.filter(clients=user_pk)        
        for a in basket:
            BoughtProduct.objects.create(quantity=a.order_quantity, color=a.color, size=a.size, clients=a.clients, products=a.products, price=a.price, subtotal=a.subtotal)

        Order.objects.filter(clients=user_pk).delete()
        total_value = sum([x.subtotal for x in basket])       
        context = {'bought':basket, 'total':total_value}
        purchase_signal.send(sender=request.user, user=request.user, context=context)
        return render(request, 'bought.html', context)

class Bought(View):
    def get(self, request, user_pk):        
        return render(request, 'bought.html')

class DeleteOrder(DeleteView):

    def get(self, request, user_pk, order_pk):
        order_to_delete = Order.objects.get(pk=order_pk)
        context = {'order_to_delete':order_to_delete}
        return render(request, 'delete_order.html', context)
    
    def post(self, request, user_pk, order_pk):        
        order = Order.objects.get(pk=order_pk)
        products_id = order.products.id
        product_query = Product.objects.get(pk=products_id)        
        color_id = order.color
        color_query = Color.objects.get(color=color_id)
        size = order.size
        quantity_back_to_stock = order.order_quantity
        Stock.objects.create(product=product_query, color=color_query, size=size, quantity=quantity_back_to_stock)    
        
        Order.objects.filter(pk=order_pk).delete()
        basket = Order.objects.filter(clients=user_pk)
        total_value = sum([x.subtotal for x in basket])        
        context = {'basket':basket, 'total':total_value}
        return render(request, 'basket.html', context)    

def test(request):
    pass    

