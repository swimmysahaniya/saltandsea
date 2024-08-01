from django.shortcuts import render
from .models import Destination, Gallery, Blog, TourPackage, Testimonial, Clients, Faqs, HomeAbout, Achievements
from django.core.paginator import Paginator
from itertools import groupby
from django.db.models import Count
from django.db.models import Q

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .forms import ContactForm, TourBookingForm
from django.template.loader import render_to_string


def home(request):

    galleries = Gallery.objects.all()
    blogs = Blog.objects.all()[:4]
    destinations = Destination.objects.all()[:10]
    testimonial = Testimonial.objects.all()
    client = Clients.objects.all()
    faqs = Faqs.objects.all()
    home_about = HomeAbout.objects.all()
    achievements = Achievements.objects.all()

    tour_package = TourPackage.objects.all()[:2]

    links = Destination.objects.all().order_by('india_part', 'state', 'destination_name')
    grouped_links = {}
    for india_part, india_part_group in groupby(links, key=lambda x: x.india_part):
        state_grouped_links = {state: list(state_group) for state, state_group in
                               groupby(india_part_group, key=lambda x: x.state)}
        grouped_links[india_part] = state_grouped_links

    context = {
        'page': 'Salt and Sea',
        'gallery': galleries,
        'blogs': blogs,
        'destinations': destinations,
        'testimonials': testimonial,
        'clients': client,
        'faqs': faqs,
        'grouped_links': grouped_links,
        'tour_packages': tour_package,
        'home_about': home_about,
        'achievements': achievements,
    }

    return render(request, "index.html", context)


def destination(request):

    galleries = Gallery.objects.all()[:9]

    queryset = Destination.objects.annotate(package_count=Count('tour_packages'))

    paginator = Paginator(queryset, 10)  # Show 10 objects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('search'):
        queryset = queryset.filter(destination_name__icontains=request.GET.get('search'))

    context = {
        'page': 'Destinations',
        'destinations': queryset,
        'page_obj': page_obj,
        'gallery': galleries,
    }

    return render(request, "destination.html", context)


def get_destination(request, slug):
    try:

        galleries = Gallery.objects.all()[:9]

        destine_place = Destination.objects.get(slug=slug)
        images = destine_place.destination_images.all()

        tour_package = destine_place.tour_packages.all()

        price_ranges = request.GET.getlist('price_range')

        # Handle price range filtering
        if price_ranges:
            price_filter = Q()
            if '1' in price_ranges:
                price_filter |= Q(price__lte=40000)
            if '2' in price_ranges:
                price_filter |= Q(price__gt=40000, price__lte=80000)
            if '3' in price_ranges:
                price_filter |= Q(price__gt=80000, price__lte=125000)
            if '4' in price_ranges:
                price_filter |= Q(price__gt=125000, price__lte=160000)
            if '5' in price_ranges:
                price_filter |= Q(price__gt=160000)

            tour_package = tour_package.filter(price_filter).distinct()

        paginator = Paginator(tour_package, 10)  # Show 10 objects per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Handle search by name
        if request.GET.get('search'):
            tour_package = tour_package.filter(name__icontains=request.GET.get('search'))

        # Handle search by date
        if request.GET.get('date_search'):
            tour_package = tour_package.filter(date_of_travel=request.GET.get('date_search'))

        context = {
            'page': slug,
            'destine_place': destine_place,
            'images': images,
            'tour_packages': tour_package,
            'page_obj': page_obj,
            'gallery': galleries,
        }
        return render(request, "tour-package.html", context)
    except Exception as e:
        print(e)
        # Render an error page
        return render(request, "error.html", {'message': 'Destination not found or an error occurred'}, status=404)


def tour_package_detail(request, slug):

    galleries = Gallery.objects.all()[:9]

    package = TourPackage.objects.get(slug=slug)
    images = package.tour_images.all()

    if request.method == 'POST':
        form = TourBookingForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            pref_travel_date = form.cleaned_data['pref_travel_date']
            message = form.cleaned_data['message']

            # Render the HTML email template
            html_message = render_to_string('email-templates/tour-booking.html', {
                'location': location,
                'name': name,
                'email': email,
                'phone': phone,
                'pref_travel_date': pref_travel_date,
                'message': message,
            })

            # Send email
            send_mail(
                'Tour Booking Enquiry',
                '',  # Plain text message (optional)
                'sahaniyaswimmy@gmail.com',
                [email],
                fail_silently=False,
                html_message=html_message,
            )

            # Redirect to a new URL
            return HttpResponseRedirect('/thanks/')
    else:
        form = TourBookingForm()

    context = {
        'page': 'Tour Packages Detail',
        'package': package,
        'images': images,
        'form': form,
        'gallery': galleries,
    }

    return render(request, "tour-package-detail.html", context)


def about(request):
    queryset = Gallery.objects.all()[:9]
    context = {'page': 'About', 'gallery': queryset}
    return render(request, "about.html", context)


def gallery(request):

    queryset = Gallery.objects.all()

    context = {'page': 'Gallery', 'gallery': queryset}
    return render(request, "gallery.html", context)


def blog(request):

    galleries = Gallery.objects.all()[:9]

    queryset = Blog.objects.all()
    paginator = Paginator(queryset, 10)  # Show 10 objects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page': 'Blog', 'blogs': queryset, 'page_obj': page_obj, 'gallery': galleries}
    return render(request, "blog.html", context)


def get_blog(request, slug):

    galleries = Gallery.objects.all()[:9]

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
        'gallery': galleries,
    }
    return render(request, "blog-detail.html", context)


def contact(request):

    queryset = Gallery.objects.all()[:9]

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            mobile_number = form.cleaned_data['mobile_number']
            message = form.cleaned_data['message']

            # Render the HTML email template
            html_message = render_to_string('email-templates/contact-form-template.html', {
                'name': name,
                'email': email,
                'mobile_number': mobile_number,
                'message': message,
            })

            # Send email
            send_mail(
                'Contact Enquiry',
                '',  # Plain text message (optional)
                'sahaniyaswimmy@gmail.com',
                [email],
                fail_silently=False,
                html_message=html_message,
            )

            # Redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'page': 'Contact', 'form': form, 'gallery': queryset})


def terms_and_conditions(request):
    galleries = Gallery.objects.all()[:9]
    context = {'page': 'Terms and Conditions', 'gallery': galleries}
    return render(request, "terms-and-conditions.html", context)


def privacy_policy(request):
    galleries = Gallery.objects.all()[:9]
    context = {'page': 'Privacy Policy', 'gallery': galleries}
    return render(request, "privacy-policy.html", context)
