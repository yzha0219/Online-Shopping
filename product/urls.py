from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('category/products/<slug:categoryslug>/', views.CategoryProductList.as_view()),
    path('category/products/', views.CategoryProductList.as_view()),
    path('category/products/detail/<int:pk>/', views.ProductListDetail.as_view())
]

# urlpatterns = format_suffix_patterns(urlpatterns)
