import re

from .models import CategoryMatcher


def rematch_orders(orders):
    # compile our regexes
    matchers = []
    for cm in CategoryMatcher.objects.all():
        matcher = {"regexp": re.compile(cm.regexp, re.IGNORECASE), "string": cm.regexp, "category": cm.category}
        matchers.append(matcher)

    for order in orders:
        for item in order.items.all():
            matched = False
            for m in matchers:
                if not matched:
                    if re.match(m["regexp"], item.description):
                        # print('matched', m['string'], 'with', item.description)
                        item.category = m["category"]
                        item.save()
                        matched = True
