from django.contrib import admin
from .models import (Destination, DestinationImage, Gallery, Blog, Review, Profile, TourPackage, TourImage,
                     Testimonial, Faqs, HomeAbout, Achievements, SEO, TemplePackage, TempleImage,
                     PrivacyPolicy, TermsNConditions)


class DestinationImageAdmin(admin.StackedInline):
    model = DestinationImage


class DestinationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('destination_name',)}
    list_display = ('category', 'india_part', 'state', 'destination_name', 'tags')
    search_fields = ('india_part', 'state', 'destination_name', 'tags', 'created_at')
    list_filter = ('category', 'india_part', 'state', 'tags', 'created_at')
    inlines = [DestinationImageAdmin]


admin.site.register(Destination, DestinationAdmin)
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
    list_display = ('destination', 'name', 'price', 'duration', 'date_of_travel')
    search_fields = ('destination__destination_name', 'name', 'created_at')
    list_filter = ('created_at',)
    inlines = [TourImageAdmin]


admin.site.register(TourPackage, TourPackageAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')


admin.site.register(Testimonial, TestimonialAdmin)


class HomeAboutAdmin(admin.ModelAdmin):
    list_display = ('short_heading', 'large_heading')


admin.site.register(HomeAbout, HomeAboutAdmin)


class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')


admin.site.register(Achievements, AchievementsAdmin)
admin.site.register(SEO)
admin.site.register(PrivacyPolicy)
admin.site.register(TermsNConditions)


class TempleImageAdmin(admin.StackedInline):
    model = TempleImage


class TemplePackageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'duration', 'date_of_travel')
    search_fields = ('name', 'created_at')
    list_filter = ('name', 'created_at')
    inlines = [TempleImageAdmin]


admin.site.register(TemplePackage, TemplePackageAdmin)
