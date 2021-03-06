from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import View, generic

from cart.forms import CartAddProductForm
from image.models import Images
from .models import Category, Product


# Create your views here.


class IndexView(View):
    template_name = 'product/index.html'

    def get_context(self):
        firstCategories = Category.firstlevelcategory(Category)
        context = {
            'firstcategorylist': firstCategories,
        }
        return context

    def get(self, request):
        context = self.get_context()
        context['haslogged'] = request.get_signed_cookie('username', default=None, salt=settings.COOKIE_SALT_VALUE,
                                                         max_age=settings.COOKIE_EXPIRE_TIME)
        return render(request, self.template_name, context)


class CategoryProductList(generic.ListView):
    # queryset = Product.objects.all()
    # context_object_name = 'productlist'
    # paginate_by = 3
    template_name = 'product/categorylist.html'
    eachby = []

    def eachbyrenew(self, itemby):
        if itemby is not None:
            try:
                itemby = int(itemby)
            except ValueError:
                itemby = 4
            try:
                itemby = 12//itemby
            except ZeroDivisionError:
                itemby = 4
            self.eachby.clear()
            self.eachby.append(itemby)

    def get_context(self, request, categoryslug):
        firstCategories = Category.firstlevelcategory(Category)
        if categoryslug == 'all':
            productlist = Product.objects.all()
        else:
            language = request.LANGUAGE_CODE
            category = get_object_or_404(Category,
                                         translations__language_code=language,
                                         translations__slug=categoryslug)
            productlist = category.categoryproductlist()
        context = {
            'firstcategorylist': firstCategories,
            'productlist': productlist,
        }
        return context

    def get(self, request, *args, **kwargs):
        categoryslug = kwargs.get('categoryslug', 'all')
        context = self.get_context(request, categoryslug)
        productlist = context['productlist']
        itemby = self.request.GET.get('eachby')
        self.eachbyrenew(itemby)
        if len(self.eachby) != 0:
            context['eachby'] = self.eachby[0]
            paginator = Paginator(productlist, self.eachby[0])
        else:
            context['eachby'] = 4
            paginator = Paginator(productlist, 4)

        page = self.request.GET.get('page', 1)
        try:
            currentPage = int(page)
            productlist = paginator.get_page(currentPage)
            if currentPage > paginator.num_pages:
                context['current_page_num'] = paginator.num_pages
            else:
                context['current_page_num'] = currentPage
        except PageNotAnInteger:
            # print("you are coming here?")
            productlist = paginator.get_page(1)
            context['current_page_num'] = 1
        except EmptyPage:
            # print("you are coming here??")
            productlist = paginator.get_page(paginator.num_pages)
        context['productlist'] = productlist.object_list
        context['paginator'] = paginator
        context['has_previous_page'] = productlist.has_previous()
        context['has_next_page'] = productlist.has_next()
        if productlist.has_previous():
            context['previous_page_number'] = productlist.previous_page_number()
        if productlist.has_next():
            context['next_page_number'] = productlist.next_page_number()
        context['page_range'] = paginator.num_pages
        context['haslogged'] = request.get_signed_cookie('username', default=None, salt=settings.COOKIE_SALT_VALUE,
                                                         max_age=settings.COOKIE_EXPIRE_TIME)
        # context['productlist'] = productlist
        # print(context)
        return render(request, self.template_name, context)


class ProductListDetail(generic.DetailView):
    template_name = 'product/productdetail.html'
    imagesets = {}

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        productinstance = get_object_or_404(Product, pk=pk)
        images = Images.getallimagesforproduct(Images, productinstance)
        self.imagesets.clear()
        self.imagesets['product'] = productinstance
        self.imagesets['otherimages'] = images
        self.imagesets['haslogged'] = request.get_signed_cookie('username', default=None,
                                                                salt=settings.COOKIE_SALT_VALUE,
                                                                max_age=settings.COOKIE_EXPIRE_TIME)
        cart_product_form = CartAddProductForm()
        # print(productinstance.categorynameforproduct())
        return render(request, self.template_name, {**{'cart_product_form': cart_product_form}, **self.imagesets})