from django.shortcuts import render
from .models import (Destination, Gallery, Blog, TourPackage, Testimonial, Clients, Faqs,
                     HomeAbout, Achievements, SEO, TemplePackage)
from django.core.paginator import Paginator
from itertools import groupby
from django.db.models import Count, Q

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .forms import ContactForm, TourBookingForm
from django.template.loader import render_to_string


def home(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="home")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    galleries = Gallery.objects.all()[:9]
    home_gallery = Gallery.objects.all()[:8]
    blogs = Blog.objects.all()[:2]
    #destinations = Destination.objects.all()[:10]
    testimonial = Testimonial.objects.all()
    client = Clients.objects.all()
    faqs = Faqs.objects.all()
    home_about = HomeAbout.objects.all()
    achievements = Achievements.objects.all()

    tour_package = TourPackage.objects.all()[:2]

    destinations = Destination.objects.annotate(package_count=Count('tour_packages'))[:10]

    links = Destination.objects.all().order_by('category', 'india_part', 'state', 'destination_name')
    grouped_links = {}
    for category, category_group in groupby(links, key=lambda x: x.category):
        india_part_grouped_links = {}
        for india_part, india_part_group in groupby(category_group, key=lambda x: x.india_part):
            state_grouped_links = {state: list(state_group) for state, state_group in
                                   groupby(india_part_group, key=lambda x: x.state)}
            india_part_grouped_links[india_part] = state_grouped_links
        grouped_links[category] = india_part_grouped_links

    temple_packages = TemplePackage.objects.all().order_by('name')

    if request.method == 'POST':
        form = TourBookingForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            no_of_nights = form.cleaned_data['no_of_nights']
            no_of_adults = form.cleaned_data['no_of_adults']
            no_of_children = form.cleaned_data['no_of_children']
            message = form.cleaned_data['message']

            # Render the HTML email template
            html_message = render_to_string('email-templates/tour-booking.html', {
                'location': location,
                'name': name,
                'email': email,
                'phone': phone,
                'no_of_nights': no_of_nights,
                'no_of_adults': no_of_adults,
                'no_of_children': no_of_children,
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
        'page': 'Salt and Sea',
        'gallery': galleries,
        'home_gallery': home_gallery,
        'blogs': blogs,
        'destinations': destinations,
        'testimonials': testimonial,
        'clients': client,
        'faqs': faqs,
        'form': form,
        'grouped_links': grouped_links,
        'temple_packages': temple_packages,
        'tour_packages': tour_package,
        'home_about': home_about,
        'achievements': achievements,
        'title': seo_data.title if seo_data else 'Salt and Sea',
        'keywords': seo_data.keywords if seo_data else 'Salt and Sea',
        'description': seo_data.description if seo_data else 'Salt and Sea',
    }

    return render(request, "index.html", context)


def destination(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="national-destination")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    queryset = (Destination.objects.filter(category="National").annotate(package_count=Count('tour_packages'))
                .order_by('destination_name'))

    if request.GET.get('search'):
        queryset = queryset.filter(destination_name__icontains=request.GET.get('search'))

    paginator = Paginator(queryset, 9)  # Show 9 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Destinations',
        'destinations': page_obj,
        'gallery': galleries,
        'page_obj': page_obj,
        'title': seo_data.title if seo_data else 'National Destinations',
        'keywords': seo_data.keywords if seo_data else 'National Destinations',
        'description': seo_data.description if seo_data else 'National Destinations',
    }

    return render(request, "national-destination.html", context)


def international_destination(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="international-destination")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    queryset = (Destination.objects.filter(category="International").annotate(package_count=Count('tour_packages'))
                .order_by('destination_name'))

    if request.GET.get('search'):
        queryset = queryset.filter(destination_name__icontains=request.GET.get('search'))

    paginator = Paginator(queryset, 9)  # Show 9 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Destinations',
        'destinations': page_obj,
        'gallery': galleries,
        'page_obj': page_obj,
        'title': seo_data.title if seo_data else 'International Destinations',
        'keywords': seo_data.keywords if seo_data else 'International Destinations',
        'description': seo_data.description if seo_data else 'International Destinations',
    }

    return render(request, "international-destination.html", context)


def tour_packages_page(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="tour_packages_page")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    destinations = Destination.objects.all()

    # Handle form submission
    destination_id = request.GET.get('destination')
    calendar = request.GET.get('calendar')
    price = request.GET.get('price')
    no_of_days = request.GET.get('no_of_days')
    no_of_adults = request.GET.get('no_of_adults')
    no_of_children = request.GET.get('no_of_children')

    # Filter tour packages based on form inputs
    tour_package_filter = Q()
    if destination_id:
        tour_package_filter &= Q(destination_id=destination_id)
    if calendar:
        tour_package_filter &= Q(date_of_travel=calendar)
    if price:
        if price == '0':
            tour_package_filter &= Q(price__lte=40000)
        elif price == '1':
            tour_package_filter &= Q(price__gt=40000, price__lte=80000)
        elif price == '2':
            tour_package_filter &= Q(price__gt=80000, price__lte=125000)
        elif price == '3':
            tour_package_filter &= Q(price__gt=125000, price__lte=160000)
        elif price == '4':
            tour_package_filter &= Q(price__gt=160000)
    if no_of_days:
        tour_package_filter &= Q(duration=no_of_days)
    if no_of_adults:
        tour_package_filter &= Q(no_of_people=no_of_adults)
    if no_of_children:
        tour_package_filter &= Q(no_of_children=no_of_children)

    queryset = TourPackage.objects.filter(
        Q(destination__category="National") & tour_package_filter
    )

    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains=request.GET.get('search'))

    # Apply explicit ordering
    queryset = queryset.order_by('name')

    paginator = Paginator(queryset, 9)  # Show 9 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Tours',
        'destinations': destinations,
        'tours': page_obj,
        'page_obj': page_obj,
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'National Tours',
        'keywords': seo_data.keywords if seo_data else 'National Tours',
        'description': seo_data.description if seo_data else 'National Tours',
    }

    return render(request, "national-tours.html", context)


def international_tours(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="international_tours")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    destinations = Destination.objects.all()

    # Handle form submission
    destination_id = request.GET.get('destination')
    calendar = request.GET.get('calendar')
    price = request.GET.get('price')
    no_of_days = request.GET.get('no_of_days')
    no_of_adults = request.GET.get('no_of_adults')
    no_of_children = request.GET.get('no_of_children')

    # Filter tour packages based on form inputs
    tour_package_filter = Q()
    if destination_id:
        tour_package_filter &= Q(destination_id=destination_id)
    if calendar:
        tour_package_filter &= Q(date_of_travel=calendar)
    if price:
        if price == '0':
            tour_package_filter &= Q(price__lte=40000)
        elif price == '1':
            tour_package_filter &= Q(price__gt=40000, price__lte=80000)
        elif price == '2':
            tour_package_filter &= Q(price__gt=80000, price__lte=125000)
        elif price == '3':
            tour_package_filter &= Q(price__gt=125000, price__lte=160000)
        elif price == '4':
            tour_package_filter &= Q(price__gt=160000)
    if no_of_days:
        tour_package_filter &= Q(duration=no_of_days)
    if no_of_adults:
        tour_package_filter &= Q(no_of_people=no_of_adults)
    if no_of_children:
        tour_package_filter &= Q(no_of_children=no_of_children)

    queryset = TourPackage.objects.filter(
        Q(destination__category="International") & Q(tour_package_filter)
    )

    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains=request.GET.get('search'))

    # Apply explicit ordering
    queryset = queryset.order_by('name')

    paginator = Paginator(queryset, 9)  # Show 9 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Tours',
        'destinations': destinations,
        'tours': page_obj,
        'page_obj': page_obj,
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'International Tours',
        'keywords': seo_data.keywords if seo_data else 'International Tours',
        'description': seo_data.description if seo_data else 'International Tours',
    }

    return render(request, "international-tours.html", context)


def get_destination(request, slug):
    try:

        # Fetch SEO data
        seo_data_qs = SEO.objects.filter(page_name=slug)
        if seo_data_qs.exists():
            seo_data = seo_data_qs.first()
        else:
            seo_data = None

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
            'title': seo_data.title if seo_data else 'Tour Packages',
            'keywords': seo_data.keywords if seo_data else 'Tour Packages',
            'description': seo_data.description if seo_data else 'Tour Packages',
        }
        return render(request, "tour-package.html", context)
    except Exception as e:
        print(e)
        # Render an error page
        return render(request, "error.html", {'message': 'Destination not found or an error occurred'}, status=404)


def tour_package_detail(request, slug):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name=slug)
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

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
            no_of_nights = form.cleaned_data['no_of_nights']
            no_of_adults = form.cleaned_data['no_of_adults']
            no_of_children = form.cleaned_data['no_of_children']
            message = form.cleaned_data['message']

            # Render the HTML email template
            html_message = render_to_string('email-templates/tour-booking.html', {
                'location': location,
                'name': name,
                'email': email,
                'phone': phone,
                'no_of_nights': no_of_nights,
                'no_of_adults': no_of_adults,
                'no_of_children': no_of_children,
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
        'title': seo_data.title if seo_data else 'Tour Packages Detail',
        'keywords': seo_data.keywords if seo_data else 'Tour Packages Detail',
        'description': seo_data.description if seo_data else 'Tour Packages Detail',
    }

    return render(request, "tour-package-detail.html", context)


def about(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="about")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    queryset = Gallery.objects.all()[:9]

    context = {
        'page': 'About',
        'gallery': queryset,
        'title': seo_data.title if seo_data else 'About',
        'keywords': seo_data.keywords if seo_data else 'About',
        'description': seo_data.description if seo_data else 'About',
    }
    return render(request, "about.html", context)


def gallery(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="gallery")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    queryset = Gallery.objects.all()

    context = {
        'page': 'Gallery',
        'gallery': queryset,
        'title': seo_data.title if seo_data else 'Gallery',
        'keywords': seo_data.keywords if seo_data else 'Gallery',
        'description': seo_data.description if seo_data else 'Gallery',
    }
    return render(request, "gallery.html", context)


def blog(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="blog")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    galleries = Gallery.objects.all()[:9]

    queryset = Blog.objects.all()
    paginator = Paginator(queryset, 9)  # Show 10 objects per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page': 'Blog',
        'blogs': queryset,
        'page_obj': page_obj,
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'Blog',
        'keywords': seo_data.keywords if seo_data else 'Blog',
        'description': seo_data.description if seo_data else 'Blog',
    }
    return render(request, "blog.html", context)


def get_blog(request, slug):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name=slug)
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

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
        'title': seo_data.title if seo_data else 'Blog Detail',
        'keywords': seo_data.keywords if seo_data else 'Blog Detail',
        'description': seo_data.description if seo_data else 'Blog Detail',
    }
    return render(request, "blog-detail.html", context)


def contact(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="contact")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

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

    context = {
        'page': 'Contact',
        'form': form,
        'gallery': queryset,
        'title': seo_data.title if seo_data else 'Contact',
        'keywords': seo_data.keywords if seo_data else 'Contact',
        'description': seo_data.description if seo_data else 'Contact',
    }

    return render(request, 'contact.html', context)


def terms_and_conditions(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="terms_and_conditions")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Terms and Conditions',
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'Terms and Conditions',
        'keywords': seo_data.keywords if seo_data else 'Terms and Conditions',
        'description': seo_data.description if seo_data else 'Terms and Conditions',
    }
    return render(request, "terms-and-conditions.html", context)


def privacy_policy(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="privacy_policy")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Privacy Policy',
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'Privacy Policy',
        'keywords': seo_data.keywords if seo_data else 'Privacy Policy',
        'description': seo_data.description if seo_data else 'Privacy Policy',
    }
    return render(request, "privacy-policy.html", context)


def thanks(request):

    galleries = Gallery.objects.all()[:9]

    context = {
        'gallery': galleries,
    }
    return render(request, "thanks.html", context)


def temple_darshan(request):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name="temple_darshan")
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    queryset = TemplePackage.objects.all().order_by('name')

    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains=request.GET.get('search'))

    paginator = Paginator(queryset, 9)  # Show 9 objects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    galleries = Gallery.objects.all()[:9]

    context = {
        'page': 'Temple Darshan',
        'destinations': queryset,
        'temple_darshan': page_obj,
        'page_obj': page_obj,
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'Temple Darshan',
        'keywords': seo_data.keywords if seo_data else 'Temple Darshan',
        'description': seo_data.description if seo_data else 'Temple Darshan',
    }

    return render(request, "temple-darshan.html", context)


def temple_darshan_detail(request, slug):

    # Fetch SEO data
    seo_data_qs = SEO.objects.filter(page_name=slug)
    if seo_data_qs.exists():
        seo_data = seo_data_qs.first()
    else:
        seo_data = None

    galleries = Gallery.objects.all()[:9]

    package = TemplePackage.objects.get(slug=slug)
    images = package.temple_images.all()

    if request.method == 'POST':
        form = TourBookingForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            no_of_nights = form.cleaned_data['no_of_nights']
            no_of_adults = form.cleaned_data['no_of_adults']
            no_of_children = form.cleaned_data['no_of_children']
            message = form.cleaned_data['message']

            # Render the HTML email template
            html_message = render_to_string('email-templates/tour-booking.html', {
                'location': location,
                'name': name,
                'email': email,
                'phone': phone,
                'no_of_nights': no_of_nights,
                'no_of_adults': no_of_adults,
                'no_of_children': no_of_children,
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
        'page': 'Temple Darshan Detail',
        'package': package,
        'images': images,
        'form': form,
        'gallery': galleries,
        'title': seo_data.title if seo_data else 'Temple Darshan Detail',
        'keywords': seo_data.keywords if seo_data else 'Temple Darshan Detail',
        'description': seo_data.description if seo_data else 'Temple Darshan Detail',
    }

    return render(request, "temple-darshan-detail.html", context)