from rest_framework.serializers import ModelSerializer

from alaris.models import Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id',
                  'alaris_product_id',
                  'acc_currency_code',
                  'alaris_acc_id',
                  'carrier',
                  'is_active',
                  'product_caption',
                  'product_description',
                  'product_notes',
                  'product_type',
                  'last_update_time',
                  ]
