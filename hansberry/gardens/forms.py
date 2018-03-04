from django.forms import ModelForm
from .models import Garden


class GardenForm(ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        # set the user as an attribute of the form
        self.user = kwargs.pop('user')
        super(GardenForm, self).__init__(*args, **kwargs)

    # def clean_garden(self):
    #     # Get the garden name
    #     name = self.cleaned_data.get('name')

    #     # Get the garden address
    #     address = self.cleaned_data.get('address')

    #     # Check to see if any gardens already exist wih this address
    #     # and name
    #     try:
    #         match = Garden.objects.get(name=name, address=address)
    #     except Garden.DoesNotExist:
    #         # Unable to find garden with same name and address
    #         return address

    #     # A garden was found with this same address
    #     raise forms.ValidationError('Sorry, a garden with this name and address already exists.')
