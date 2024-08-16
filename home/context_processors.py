from itertools import groupby
from .models import Destination, TemplePackage


def navigation_links(request):
    links = Destination.objects.all().order_by('category', 'india_part', 'state', 'destination_name')
    grouped_links = {}
    for category, category_group in groupby(links, key=lambda x: x.category):
        india_part_grouped_links = {}
        for india_part, india_part_group in groupby(category_group, key=lambda x: x.india_part):
            state_grouped_links = {state: list(state_group) for state, state_group in groupby(india_part_group, key=lambda x: x.state)}
            india_part_grouped_links[india_part] = state_grouped_links
        grouped_links[category] = india_part_grouped_links
    return {'grouped_links': grouped_links}


def temple_navigation(request):
    temple_packages = TemplePackage.objects.all().order_by('name')
    return {'temple_packages': temple_packages}


