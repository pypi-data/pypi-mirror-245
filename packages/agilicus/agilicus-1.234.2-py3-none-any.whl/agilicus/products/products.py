from ..context import get_apiclient_from_ctx
import agilicus
import operator
from ..output.table import (
    column,
    spec_column,
    metadata_column,
    format_table,
    subtable,
)


def get_api(ctx, name, v2=False):
    client = get_apiclient_from_ctx(ctx)
    if v2:
        return getattr(client.products_api, "v2_" + name)
    return getattr(client.billing_api, name)


def list_products(ctx, v2=False, **kwargs):
    list_products = get_api(ctx, "list_products", v2)
    products = list_products(**kwargs)
    products.products = sorted(products.products, key=lambda d: d["spec"]["label"])
    return products


def format_products(ctx, products_obj):
    products = products_obj.to_dict()

    def get_product_name(record, key):
        return "{0: <20}".format(record["product"]["name"])

    def get_product_nickname(record, key):
        return "{0: <28}".format(record["nickname"])

    def get_product_metric(record, key):
        if "metric" in record["product"]["metadata"]:
            return "{0: <20}".format(record["product"]["metadata"]["metric"])
        else:
            return "{0: <20}".format("")

    def get_unit_amount(record, key):
        if record["unit_amount"]:
            return "{:,.2f}".format(record["unit_amount"] / 100)
        return ""

    product_price_column = [
        column("id", optional=True),
        column("product name", getter=get_product_name, optional=True),
        column("nickname", getter=get_product_nickname, optional=True),
        column("metric", getter=get_product_metric, optional=True),
        column("unit_amount", getter=get_unit_amount, optional=True),
    ]
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("label", optional=True),
        spec_column("description", optional=True),
        spec_column("trial_period", optional=True),
        #        spec_column("dev_mode", optional=True),
        subtable(
            ctx,
            "billing_product_prices",
            product_price_column,
            table_getter=operator.itemgetter,
            subobject_name="status",
            optional=True,
        ),
    ]
    return format_table(
        ctx, products.get("products"), columns, getter=operator.itemgetter
    )


def add_product(
    ctx,
    name=None,
    dev_mode=None,
    trial_period=None,
    product_price_ids=[],
    v2=False,
    **kwargs,
):
    create_product = get_api(ctx, "create_product", v2)
    prices = []
    for price_id in product_price_ids:
        prices.append(agilicus.BillingProductPrice(id=price_id))
    spec = agilicus.ProductSpec(name=name, billing_product_prices=prices, **kwargs)

    if dev_mode is not None:
        spec.dev_mode = dev_mode
    if trial_period is not None:
        spec.trial_period = trial_period

    product = agilicus.Product(spec=spec)

    return create_product(product)


def delete_product(ctx, product_id=None, v2=False, **kwargs):
    delete_product = get_api(ctx, "delete_product", v2)
    return delete_product(product_id)


def get_product(ctx, product_id=None, v2=False, **kwargs):
    get_product = get_api(ctx, "get_product", v2)
    return get_product(product_id)


def update_product(
    ctx,
    product_id=None,
    dev_mode=None,
    name=None,
    product_price_ids=None,
    remove_product_price_ids=None,
    label=None,
    description=None,
    trial_period=None,
    v2=False,
    **kwargs,
):
    get_product = get_api(ctx, "get_product", v2)

    product = get_product(product_id)

    if remove_product_price_ids is not None:
        old_prices = product.spec.billing_product_prices
        product.spec.billing_product_prices = []
        for price in old_prices:
            if price.id in remove_product_price_ids:
                # needs to be removed.
                continue
            product.spec.billing_product_prices.append(price)

    if product_price_ids is not None:
        for price_id in product_price_ids:
            product.spec.billing_product_prices.append(
                agilicus.BillingProductPrice(id=price_id)
            )

    if dev_mode is not None:
        product.spec.dev_mode = dev_mode
    if name is not None:
        product.spec.name = name
    if description is not None:
        product.spec.description = description
    if label is not None:
        product.spec.label = label
    if trial_period is not None:
        product.spec.trial_period = trial_period

    replace_product = get_api(ctx, "replace_product", v2)

    return replace_product(
        product_id,
        product=product,
    )
