from django.contrib import admin
from .models import Destination, DestinationImage, Gallery, Blog, Review, Profile, TourPackage, TourImage, Testimonial, Clients, Faqs


class DestinationImageAdmin(admin.StackedInline):
    model = DestinationImage


class DestinationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('destination_name',)}
    list_display = ('destination_name', 'slug')
    inlines = [DestinationImageAdmin]


admin.site.register(Destination, DestinationAdmin)
admin.site.register(DestinationImage)
admin.site.register(Gallery)
admin.site.register(Review)


class FaqsAdmin(admin.ModelAdmin):
    list_display = ('question',)


admin.site.register(Faqs, FaqsAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tags', 'category', 'created_at')
    search_fields = ('title', 'author__username', 'category')
    list_filter = ('author', 'category', 'created_at')


admin.site.register(Blog, BlogAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')


admin.site.register(Profile, ProfileAdmin)


class TourImageAdmin(admin.StackedInline):
    model = TourImage


class TourPackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    inlines = [TourImageAdmin]


admin.site.register(TourPackage, TourPackageAdmin)
admin.site.register(TourImage)
admin.site.register(Clients)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


admin.site.register(Testimonial, TestimonialAdmin)
