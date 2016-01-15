from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from app.order_shipping_address.models import OrderShippingAddress


@api_view(['GET', 'POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def addresses_list(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        if data['order_id'] is not None:
            address, created = OrderShippingAddress.objects.update_or_create(order_id=data['order_id'],
                                                                             user_id=data['user_id'])
            address.name = data['name']
            address.address = data['address']
            address.address1 = data['address1']
            address.city = data['city']
            address.state = data['state']
            address.contact_number = data['contact_number']
            address.zip_code = data['zip_code']
            address.is_default = data['is_default']
            address.save()
            return Response({'created': created, 'data': data})
        else:
            return Response({'error': 'Something went wrong'})
