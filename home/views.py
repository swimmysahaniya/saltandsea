from django.shortcuts import render
from django.http import HttpResponse
from .models import Destination, Gallery, Blog, TourPackage
from django.core.paginator import Paginator


def home(request):

    galleries = Gallery.objects.all()
    blogs = Blog.objects.all()[:4]
    destinations = Destination.objects.all()

    context = {
        'page': 'Salt and Sea',
        'gallery': galleries,
        'blogs': blogs,
        'destinations': destinations,
    }

    return render(request, "index.html", context)


def destination(request):

    queryset = Destination.objects.all()
    paginator = Paginator(queryset, 10)  # Show 10 objects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('search'):
        queryset = queryset.filter(destination_name__icontains=request.GET.get('search'))

    context = {'page': 'Destinations', 'destinations': queryset, 'page_obj': page_obj}
    return render(request, "destination.html", context)


def get_destination(request, slug):
    try:
        destine_place = Destination.objects.get(slug=slug)
        images = destine_place.destination_images.all()
        tour_package = destine_place.tour_packages.all()

        context = {
            'page': slug,
            'destine_place': destine_place,
            'images': images,
            'tour_packages': tour_package,
        }
        return render(request, "tour-package.html", context)
    except Exception as e:
        print(e)
        # Render an error page
        return render(request, "error.html", {'message': 'Destination not found or an error occurred'}, status=404)


def tour_package_detail(request, slug):

    package = TourPackage.objects.get(slug=slug)
    context = {
        'page': 'Tour Packages Detail',
        'package': package,
    }

    return render(request, "tour-package-detail.html", context)


def about(request):
    context = {'page': 'About'}
    return render(request, "about.html", context)


def gallery(request):

    queryset = Gallery.objects.all()

    context = {'page': 'Gallery', 'gallery': queryset}
    return render(request, "gallery.html", context)


def blog(request):
    queryset = Blog.objects.all()
    paginator = Paginator(queryset, 10)  # Show 10 objects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page': 'Blog', 'blogs': queryset, 'page_obj': page_obj}
    return render(request, "blog.html", context)


def get_blog(request, slug):
    blog_detail = Blog.objects.get(slug=slug)

    # Get all tags from all blogs
    all_blogs = Blog.objects.all()
    all_tags = set()
    for blogo in all_blogs:
        tags = blogo.tags.split(',')
        for tag in tags:
            all_tags.add(tag.strip())

    # Fetch reviews related to this blog
    reviews = blog_detail.reviews.all()

    # Fetch related blogs by category
    related_blogs = Blog.objects.filter(category="Popular")

    # Fetch previous and next blogs based on publication date
    previous_blog = Blog.objects.filter(created_at__lt=blog_detail.created_at).order_by('-created_at').first()
    next_blog = Blog.objects.filter(created_at__gt=blog_detail.created_at).order_by('created_at').first()

    context = {
        'page': 'Blog Detail',
        'blog_detail': blog_detail,
        'tags': all_tags,
        'reviews': reviews,
        'author': blog_detail.author,
        'author_profile': blog_detail.author.profile,
        'related_blogs': related_blogs,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
    }
    return render(request, "blog-detail.html", context)


def contact(request):
    context = {'page': 'Contact'}
    return render(request, "contact.html", context)


def terms_and_conditions(request):
    context = {'page': 'Terms and Conditions'}
    return render(request, "terms-and-conditions.html", context)


def privacy_policy(request):
    context = {'page': 'Privacy Policy'}
    return render(request, "privacy-policy.html", context)
