from django import forms

# Generally, it’s best to define choices (in this case categories_list) inside a model class, 
# and to define a suitably-named constant for each value:
categories_list = (
    ("F","Fashion"), ("T","Toys"), ("E","Electronics"), ("H","Home"),("O", "Other")
    )

class CreatePageForm(forms.Form):
    item = forms.CharField(label="Item")
    category = forms.ChoiceField(label="Category", choices = categories_list, required=False, initial="O")
    description = forms.CharField(label="description", widget=forms.Textarea)
    starting_bid = forms.DecimalField(label="starting_bid")
    image = forms.URLField(label="Image", required=False)


class CommentForm(forms.Form):
    content = forms.CharField(label="description", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    

class BidForm(forms.Form):
    bid = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        min_value = kwargs.pop('min_value')
        super().__init__(*args, **kwargs)
        self.min_value = min_value

    def validate_bid(self):
        new_bid = self.cleaned_data.get('bid')
        if new_bid < self.min_value+1:
            raise forms.ValidationError('Bid too low.')
        return new_bid