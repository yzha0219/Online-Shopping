from django.http import Http404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status

from user.api.serializers import BuyerSerializer, AdminBuyerSerializer, BuyerDetailSerializer
from user.models import Buyer


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class BuyerList(generics.CreateAPIView):
    """
    the api for user registrations
    """
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class AdminBuyerList(generics.ListAPIView):
    """
    General Method for Listing user instances including all detailed user information
    """
    queryset = Buyer.objects.all()
    serializer_class = AdminBuyerSerializer


class AdminBuyerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a buyer instance for admin user
    """
    queryset = Buyer.objects.all()
    serializer_class = AdminBuyerSerializer


class UserRegisterCheck(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    """
    The Api for checking the username/email/telephone uniqueness.\n
    example call: /username/value/ to check the value has been registered or not
    """
    serializer_class = BuyerSerializer

    def get(self, request, *args, **kwargs):

        return self.retrieve(request, *args, **kwargs)

    def get_object(self, fieldname, fieldvalue):
        retresult = {
            'Status_Code': None,
            'Verified_Field': fieldname,
            'Verified_Value': fieldvalue,
            'HaveOrNotHave': None
        }
        try:
            if fieldname == 'username':
                buyerinstance = Buyer.objects.get(username=fieldvalue)
            elif fieldname == 'mail':
                buyerinstance = Buyer.objects.get(mail=fieldvalue)
            elif fieldname == 'telephone':
                buyerinstance = Buyer.objects.get(telephone=fieldvalue)
            retresult['Status_Code'] = status.HTTP_200_OK
            retresult['HaveOrNotHave'] = True
            return retresult
        except Buyer.DoesNotExist:
            retresult['Status_Code'] = status.HTTP_204_NO_CONTENT
            retresult['HaveOrNotHave'] = None
            return retresult

    def retrieve(self, request, *args, **kwargs):
        fieldname = kwargs.get('fieldname')
        fieldvalue = kwargs.get('fieldvalue')
        retresult = self.get_object(fieldname, fieldvalue)
        # serializer = self.get_serializer(instance)
        return Response(retresult)


class BuyerDetailByName(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    """
    user profile details and update
    """
    serializer_class = BuyerDetailSerializer

    def get(self, request, username, *args, **kwargs):
        return self.retrieve(request, username, *args, **kwargs)

    def put(self, request, username, *args, **kwargs):
        return self.update(request, username, *args, **kwargs)

    def get_object(self, username):
        try:
            return Buyer.objects.get(username=username)
        except Buyer.DoesNotExist:
            raise Http404

    def retrieve(self, request, username, *args, **kwargs):
        instance = self.get_object(username)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, username, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(username)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


