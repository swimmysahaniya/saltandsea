from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User


class Destination(BaseModel):

    # Specifying the choices
    TAG_CHOICES = (
        ("New", "New"),
        ("Most Viewed", "Most Viewed"),
        ("Discounted", "Discounted"),
        ("50% Off", "50% Off"),
    )

    category = models.CharField(max_length=100, default="National", choices=(("National", "National"),
                                                                                  ("International", "International")))
    india_part = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    destination_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True, choices=TAG_CHOICES)
    description = models.TextField(null=True, blank=True)
    video_file = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.destination_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.destination_name

    def tour_package_count(self):
        return self.tour_packages.count()


class DestinationImage(BaseModel):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="destination_images")
    image = models.ImageField(upload_to="destination")


class TourPackage(BaseModel):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tour_packages')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # Duration in days
    description = models.TextField()
    t_image = models.ImageField(upload_to="tour", default="38.jpg")
    date_of_travel = models.DateField()
    no_of_people = models.IntegerField(default=0)
    no_of_children = models.IntegerField(default=0)
    map_iframe = models.CharField(max_length=255, default="")
    included = models.TextField(default="")
    not_included = models.TextField(default="")
    itinerary = models.TextField(default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TourImage(BaseModel):
    tour = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="tour_images")
    image = models.ImageField(upload_to="tour")


class Gallery(BaseModel):
    image = models.ImageField(upload_to="gallery")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Blog(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    featured_image = models.ImageField(upload_to="blog")
    description = models.TextField()
    tags = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="review")
    comment = models.TextField()

    def __str__(self):
        return f'Review for {self.blog.title} by {self.user.username}'


class Testimonial(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="testimonials")
    location = models.CharField(max_length=100)
    description = models.TextField()


class Clients(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="clients")


class Faqs(BaseModel):
    question = models.TextField()
    answer = models.TextField()


class HomeAbout(BaseModel):
    short_heading = models.CharField(max_length=50)
    large_heading = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="home_about")
    years = models.IntegerField(default=20)
    countries = models.IntegerField(default=100)


class Achievements(BaseModel):
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=100)


class SEO(models.Model):
    page_name = models.CharField(max_length=100, unique=True)  # Unique identifier for the page
    title = models.CharField(max_length=255)
    keywords = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.page_name


class TemplePackage(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)  # Duration in days
    description = models.TextField()
    t_image = models.ImageField(upload_to="temple", null=True, blank=True)
    date_of_travel = models.DateField()
    no_of_people = models.IntegerField()
    no_of_children = models.IntegerField()
    map_iframe = models.CharField(max_length=255, null=True, blank=True)
    included = models.TextField()
    not_included = models.TextField()
    itinerary = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TempleImage(BaseModel):
    temple = models.ForeignKey(TemplePackage, on_delete=models.CASCADE, related_name="temple_images")
    image = models.ImageField(upload_to="temple")

