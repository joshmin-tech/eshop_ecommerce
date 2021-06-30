from django.forms import ModelForm
from category.models import Category
from store.models import Product

class CategoryForms(ModelForm):
    class Meta:
        model=Category
        fields= '__all__'

class ProductForms(ModelForm):

    class Meta:
        model = Product
        fields =  '__all__'
