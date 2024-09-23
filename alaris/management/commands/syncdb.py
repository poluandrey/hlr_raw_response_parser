from itertools import islice

from django.core.management import BaseCommand
from django.conf import settings

from alaris.enterprise_api.schema import Product
from alaris.models import Carrier as DBCarrier, Product as DBProduct, ProductType
from alaris.enterprise_api.client import EnterpriseClient


def insert_carrier(batch_size, new_carrier):
    while True:
        batch = list(islice(new_carrier, batch_size))
        objects = [DBCarrier(
            external_id=carrier.car_id,
            name=carrier.car_name,
            is_active=carrier.car_is_active,
        ) for carrier in batch]
        if not objects:
            break

        DBCarrier.objects.bulk_create(objects)


def update_carrie(carriers: DBCarrier, existing_carriers):
    for existing_carrier in existing_carriers:
        changed = False
        carrier = carriers.get(external_id=existing_carrier.car_id)
        if carrier.name != existing_carrier.car_name:
            carrier.name = existing_carrier.car_name
            changed = True

        if carrier.is_active != existing_carrier.car_is_active:
            carrier.is_active = existing_carrier.car_is_active
            changed = True

        if changed:
            carrier.save()


def handle_client_sync(batch_size, client):
    external_carriers = client.carrier.get_all()
    external_carriers_id = {carrier.car_id for carrier in external_carriers}

    carriers = DBCarrier.objects.all()
    carriers_id = {carrier.external_id for carrier in carriers}

    new_carriers_id = external_carriers_id.difference(carriers_id)
    new_carriers = filter(lambda carrier: carrier.car_id in new_carriers_id, external_carriers)
    insert_carrier(batch_size, new_carriers)
    existing_carriers = filter(lambda carrier: carrier.car_id not in new_carriers, external_carriers)
    update_carrie(carriers=carriers, existing_carriers=existing_carriers)


def insert_product(batch_size, new_products):
    while True:
        batch = list(islice(new_products, batch_size))
        objects = [DBProduct(
            external_id=product.product_id,
            account_currency_code=product.acc_currency_code,
            external_account_id=product.acc_id,
            is_active=product.is_active,
            caption=product.product_caption,
            description=product.product_descr,
            direction=product.product_direction,
            notes=product.product_notes,
            carrier=DBCarrier.objects.get(external_id=product.car_id),
            type=ProductType.objects.get(external_id=product.product_type),
        ) for product in batch]

        if not objects:
            break

        DBProduct.objects.bulk_create(objects)


def handle_product_sync(batch_size, client):
    external_products: list[Product] = client.product.get_all()
    external_products_id = {product.product_id for product in external_products}

    products = DBProduct.objects.all()
    products_id = {product.external_id for product in products}

    new_product_id = external_products_id.difference(products_id)
    new_products = filter(lambda product: product.product_id in new_product_id, external_products)
    insert_product(batch_size, new_products)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--table-name', choices=['carrier', 'product'], required=True)
        parser.add_argument('--batch-size', default=500, help='count of records to insert')

    def handle(self, *args, **options) -> None:
        batch_size = options['batch_size']
        client = EnterpriseClient(base_url=settings.EAPI_BASE_URL, auth=settings.EAPI_AUTH)
        if options['table_name'] == 'carrier':
            handle_client_sync(batch_size, client)

        if options['table_name'] == 'product':
            handle_product_sync(batch_size, client)
