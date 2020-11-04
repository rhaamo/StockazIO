from django.core.management.base import BaseCommand
from django.conf import settings
from libs.mouser.mouser import Mouser
from controllers.OrdersImporter.models import Order, Item


def import_from_mouser(api_key, filter):
    print(f"Importing {filter} from Mouser")
    squeak = Mouser(api_key=api_key)
    # Get all orders matching the filter
    orders = squeak.order_history_by_date_filter(filter)
    if orders["NumberOfOrders"] == 0:
        print("No available orders to import")
        return

    for order in orders["OrderHistoryItems"]:
        # Check if we already have an order matching in database
        # Or fetch is already existing
        try:
            db_order = Order.objects.get(order_number=order["WebOrderNumber"], vendor="mouser")
        except Order.DoesNotExist:
            db_order = Order(
                date=order["DateCreated"],
                order_number=order["WebOrderNumber"],
                status=order["OrderStatusDisplay"],
                vendor="mouser",
                import_state=0,
            )
            db_order.save()

        print(f"Got order {db_order.order_number} from {db_order.date}")

        # if order import_state isn't 0 (Unknown, newly created), continue
        if db_order.import_state != 0:
            print(f"Order status is {db_order.import_state}, continuing to next.")
            continue

        print(f"Order status is {db_order.import_state}, fetching items.")
        # Fetch items of order now
        items = squeak.order_number(db_order.order_number)
        imported_items = 0
        for item in items["OrderLines"]:
            db_item, _ = Item.objects.get_or_create(
                vendor_part_number=item["MouserPartNumber"],
                mfr_part_number=item["MfrPartNumber"],
                manufacturer=item["Manufacturer"],
                description=item["Description"],
                quantity=item["Quantity"],
                order=db_order,
            )
            imported_items += 1
        print(f"Imported {imported_items}, API reported {len(items['OrderLines'])}")

        # Update order to Fetched
        db_order.import_state = 1
        db_order.save()


class Command(BaseCommand):
    help = "Import orders from known websites"

    def add_arguments(self, parser):
        parser.add_argument("--filter", type=str)

    def handle(self, *args, **options):
        # Mouser
        mouser_api_key = settings.MOUSER_API_KEY
        if not mouser_api_key:
            print("Not importing from Mouser, MOUSER_API_KEY undeclared")
        elif mouser_api_key:
            filter = options["filter"] if "filter" in options else None
            if not filter:
                filter = settings.MOUSER_IMPORT_FILTER
            import_from_mouser(mouser_api_key, filter)
