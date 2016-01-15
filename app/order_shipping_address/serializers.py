from rest_framework import serializers

from app.order_shipping_address.models import OrderShippingAddress


class OrderShippingAddressSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')
    user_id = serializers.IntegerField(source='User.id')


    class Meta:
        model = OrderShippingAddress
        fields = ('id', 'name', 'user_id', 'order_id', 'address', 'address1', 'city', 'state', 'zip_code', 'contact_number', 'is_default')


