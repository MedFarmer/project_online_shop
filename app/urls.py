from django.urls import path
from .views import Home, AddProduct, AddStock, test, SignUp, Logout, Users, Login, Detail, Update, Delete, AddTextile, AddColor, AddSize, AddImage, \
    AddImageDelete, Basket, DeleteOrder, DeleteColorView, Bought, Index, get_available_sizes, get_available_quantities

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('home/', Home.as_view(), name='home'),
    path('addgoods/', AddProduct.as_view(), name='addproduct'),
    path('addstock/', AddStock.as_view(), name='addstock'),
    path('addtextile/', AddTextile.as_view(), name='addtextile'),
    path('addcolor/', AddColor.as_view(), name='addcolor'),
    path('addcolor/delete_color/<int:pk>/', DeleteColorView.as_view(), name='delete_color'),
    path('addsize/', AddSize.as_view(), name='addsize'),    
    path('test/', test, name='test'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/', Users.as_view(), name='users'),
    path('detail/<int:pk>/', Detail.as_view(), name='detail'),
    path('detail/<int:pk>/update/', Update.as_view(), name='update'),
    path('detail/<int:pk>/delete/', Delete.as_view(), name='delete'),
    path('get-available-sizes/', get_available_sizes, name='get-available-sizes'),
    path('get-available-quantities/',get_available_quantities, name='get-available-quantities'),    
    path('addgoods/<int:product_pk>/addimage/', AddImage.as_view(), name='addimage'),
    path('addgoods/<int:product_pk>/addimage/<int:image_pk>/delete/', AddImageDelete.as_view(), name='addimage_delete'),
    path('basket/<int:user_pk>/', Basket.as_view(), name='basket'),
    path('basket/<int:user_pk>/delete_order/<int:order_pk>/', DeleteOrder.as_view(), name='delete_order'),
    path('basket/<int:user_pk>/bought/', Bought.as_view(), name='bought'),
]

