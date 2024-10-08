from django.forms import ModelForm
from django import forms
from .models import Project, Review

# Create your forms here.


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = ['__all__']
        fields = ['title', 'description', 'demo_link',
                  'source_link', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        self.fields['featured_image'].widget.attrs.update(
            {'class': 'form__field--image'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
