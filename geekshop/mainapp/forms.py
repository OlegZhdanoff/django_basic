from django import forms
from mainapp import models


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = models.Products
        # fields = '__all__'
        fields = ('photo', 'name', 'price', 'description', 'category', 'is_visible')
        # widgets = {
        #     'photo': forms.ImageField(attrs={'class': 'form-control'}),
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'price': forms.DecimalField(attrs={'class': 'form-control'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
        #     'category': forms.Select(attrs={'class': 'form-control'}),
        #     'is_visible': forms.CheckboxInput(attrs={'class': "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = 'custom-file-input'
