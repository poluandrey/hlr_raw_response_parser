from rest_framework.serializers import ModelSerializer

from alaris.models import Product


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id',
                  'external_id',
                  'account_currency_code',
                  'external_account_id',
                  'carrier',
                  'is_active',
                  'caption',
                  'description',
                  'notes',
                  'type',
                  'last_update_time',
                  ]
