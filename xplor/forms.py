from django import forms
from xplor.models import Itinerary, Category
from multiupload.fields import MultiFileField

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class ItineraryForm(forms.ModelForm):
    name = forms.CharField(max_length=140, help_text="Please enter the name of the itinerary.")
    location = forms.CharField(max_length=140, help_text="Enter the location of the trip.")
    date = forms.DateField()
    reservation_deadline = forms.DateField()
    tags = forms.Textarea()
    description = forms.Textarea()    
    price = forms.DecimalField()
    slots = forms.IntegerField(min_value=1)
    days_duration = forms.IntegerField()
    nights_duration = forms.IntegerField()
    isPrivate = forms.BooleanField()
    isRecurring = forms.BooleanField()
    category = forms.Select()
    image = forms.FileField()

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Itinerary

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('pub_date',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')