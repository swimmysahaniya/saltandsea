from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)


class TourBookingForm(forms.Form):
    location = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    pref_travel_date = forms.DateField()
    message = forms.CharField(widget=forms.Textarea, required=False)

