from django import template
import math

register = template.Library()

@register.simple_tag
def discount_calculation(price,discount):
    if discount is None or discount is 0:
        return price
    price = float(price)
    discount = float(discount)
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(sellprice)

@register.filter
def mul(value, arg):
    return float(value) * arg


@register.filter
def div(value, arg):
    """Divide value by arg, return 0 if arg is 0."""
    try:
        return float(value) / float(arg)
    except (ZeroDivisionError, ValueError):
        return 0
