import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View, generic

from cart.cart import Cart
from product.models import Product
from user.models import User, UserInfoEntity
from .forms import OrderCreateForm
from .models import Order, OrderItem


# Create your views here.


class orderpreview(View):
    template_name = 'order/ordercreate.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        ownerinstance = get_object_or_404(User, pk=3)
        userinfo = kwargs.get('userinfo', None)
        if userinfo is not None:
            userinfoinstance = get_object_or_404(UserInfoEntity, name=userinfo)
            ordercreateform = OrderCreateForm(initial={'name': userinfoinstance.name, 'email': userinfoinstance.mail,
                                                       'telephone': userinfoinstance.telephone,
                                                       'postal': userinfoinstance.recaddresspostal,
                                                       'address': userinfoinstance.recaddress})
        else:
            ordercreateform = OrderCreateForm()
        # self.get_form_kwargs(ownerinstance)
        return render(request, self.template_name, {'ordercreateform': ordercreateform,
                                                    'cart': cart, 'owner': ownerinstance})


class ordercreate(View):
    template_name = 'order/ordercreate.html'

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        ownerinstance = get_object_or_404(User, pk=3)
        ordercreateform = OrderCreateForm(request.POST)
        if ordercreateform.is_valid():
            cd = ordercreateform.cleaned_data
            name = cd['name']
            email = cd['email']
            telephone = cd['telephone']
            postal = cd['postal']
            address = cd['address']
            ordercreate = Order.objects.create(owner=ownerinstance, order_receiver_name=name, order_email=email,
                                               order_telephone=telephone, order_receiver_address_postal=postal,
                                               order_receiver_address=address)
            for item in cart.cart:
                product = get_object_or_404(Product, pk=item)
                quantity = cart.cart.get(item)['quantity']
                price = cart.cart.get(item)['price']
                orderitem = OrderItem.objects.create(order=ordercreate, product=product, quantity=quantity,
                                                     price=price)
                request.session['order_id'] = ordercreate.id
            cart.clear()
            return redirect(reverse('payment:payment_process'))
            # return redirect('order:order_preview')
        else:
            return redirect('order:order_preview')


class orderreview(View):
    """
    review the detail order list by order id
    """
    template_name = 'order/ordercreated.html'

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        orderdetailinstance = get_object_or_404(Order, pk=order_id)
        return render(request, self.template_name, {'orderdetailview': orderdetailinstance})


class orderlist(generic.ListView):
    """
    List all order for one specific user
    """
    template_name = 'order/orderlist.html'

    def get(self, request):
        status_order = request.GET.get('status', 'all')
        ownerinstance = get_object_or_404(User, pk=3)
        if status_order == 'all':
            orderlist = ownerinstance.own_orders.all()
        elif status_order == 'paid':
            orderlist = ownerinstance.own_orders.filter(status_order='paid')
        elif status_order == 'unpaid':
            orderlist = ownerinstance.own_orders.filter(status_order='unpaid')
        elif status_order == 'delete':
            orderlist = ownerinstance.own_orders.filter(status_order='delete')
        elif status_order == 'cancel':
            orderlist = ownerinstance.own_orders.filter(status_order='cancel')
        # for order in orderlist:
        #     print(order.get_top2_orderitems())
        return render(request, self.template_name, {'orderlist': orderlist})


def print_to_pdf(request, *args, **kwargs):
    order_id = kwargs.get('pk')
    orderinstance = get_object_or_404(Order, pk=order_id)
    html = render_to_string('order/order_pdf.html', {'order': orderinstance})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(orderinstance.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0] + 'css/pdf.css')])
    return response