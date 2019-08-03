
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name='home'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contactus'),
    path("tracker/",views.tracker,name='trackingstatus'),
    path("search/",views.search,name='search'),
    path("productview/<int:id>/",views.productview,name='productview'),
    path("checkout/",views.checkout,name='checkout'),
    
]