from django.core.paginator import Paginator

ITEMS_PER_PAGE = 12


def get_page(request, queryset, per_page=ITEMS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))
