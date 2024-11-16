"""
URL configuration for sweet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path,include

from sweet import views

urlpatterns = [
    
    # path('admin/', admin.site.urls),
    path('', views.home),
    path('admin/', views.admin_panel),
    path('login/', views.user_login),
    path('signup/', views.user_signup),
    path('logout/', views.user_logout),
    path('flavour/<flavour_value>', views.filter_by_flavour),
    path('weight/<weight_value>', views.filter_by_weight),
    path('event/<event_value>', views.filter_by_event),
    path('shape/<shape_value>', views.filter_by_shape),
    path('sort/<sort_value>', views.sort_by_price),
    path('search/', views.search_by_price_range),
    path('chocolate/<chocolate_id>', views.add_to_cart),    
    path('cart/', views.show_cart),
    path('cart/delete/<cart_id>', views.delete_cart),
    path('cart/update/<flag>/<cart_id>', views.update_cart_quantity),    
    path('order/', views.show_order),
    path('variety/',views.variety),
    path('admin/chocolate/', include('chocolate.chocolate_urls')),    
    path('make-payment/', views.make_payment),
    path('forgotpassword',views.forgot_password),
    path('forgotpassword/update/<uname>',views.passotp),
]



