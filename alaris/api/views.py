from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from alaris.api.serializers import ProductSerializer
from alaris.models import Product


class ProductView(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(responses=ProductSerializer(many=True))
    @action(methods=['get'], detail=False)
    def hlr(self):
        hlr_product = Product.objects.filter(product_type__type_name='HLR')
        serializer = ProductSerializer(hlr_product, many=True)

        return Response(serializer.data)
