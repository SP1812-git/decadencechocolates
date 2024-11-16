from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from chocolate import views
urlpatterns = [
    path('add/', views.add_chocolate),
    path('view/', views.view_chocolates),
    path('update/<chocolateid>',views.update_chocolate),
    path('delete/<chocolateid>',views.delete_chocolate),

    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)