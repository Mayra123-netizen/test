from django.urls import path
from . import views

urlpatterns = [
    path('Buyersignup', views.Buyersignup.as_view()),
    path('Sellersignup', views.Sellersignup.as_view()),
    path('Buyerlogin', views.Buyerlogin.as_view()),
    path('Sellerlogin', views.Sellerlogin.as_view()),
    path('uploaditem', views.Uploaditem.as_view()),  
    path('viewitems', views.Viewitem.as_view()),  
    path('searchitem', views.Searchitem.as_view()),  
    path('deleteitem', views.Deleteitem.as_view()),  
    path('updateitem', views.Updateitem.as_view()),
    path('Logout', views.Logout.as_view()),

]
#     path('Buyerlogout', views.BuyerLogout.as_view()),
#     path('Sellerlogout', views.SellerLogout.as_view()),
#     path('Updateitem', views.Updateitem.as_view()), 
# 
