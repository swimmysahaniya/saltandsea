from itertools import groupby
from .models import Destination


def navigation_links(request):
    links = Destination.objects.all().order_by('india_part', 'state', 'destination_name')
    grouped_links = {}
    for india_part, india_part_group in groupby(links, key=lambda x: x.india_part):
        state_grouped_links = {state: list(state_group) for state, state_group in groupby(india_part_group, key=lambda x: x.state)}
        grouped_links[india_part] = state_grouped_links
    return {'grouped_links': grouped_links}

