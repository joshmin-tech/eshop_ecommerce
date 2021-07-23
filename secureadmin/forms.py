from django.forms import ModelForm
from category.models import Category
from store.models import Product





class CategoryForms(ModelForm):
    class Meta:
        model=Category
        fields= '__all__'
    def __init__(self, *args, **kwargs):
        super(CategoryForms, self).__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs.update({'class': "form-control"})
        self.fields['description'].widget.attrs.update({'class': "form-control"})
        self.fields['slug'].widget.attrs.update({'class': "form-control"})
      
        




class ProductForms(ModelForm):

    class Meta:
        model = Product
        fields =  '__all__'
    def __init__(self, *args, **kwargs):
        super(ProductForms, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': "form-control"})
        self.fields['product_name'].widget.attrs.update({'class': "form-control"})
        self.fields['slug'].widget.attrs.update({'class': "form-control"})
        self.fields['price'].widget.attrs.update({'class': "form-control"})
        self.fields['brand'].widget.attrs.update({'class': "form-control"})
        self.fields['stock'].widget.attrs.update({'class': "form-control"})
        self.fields['is_available'].widget.attrs.update({'class': "form-check-input"})
        self.fields['description'].widget.attrs.update({'class': "form-control"})
        self.fields['images1'].widget.attrs.update({'class': "form-control"})
        self.fields['images2'].widget.attrs.update({'class': "form-control"})
        self.fields['images3'].widget.attrs.update({'class': "form-control"})
        self.fields['images4'].widget.attrs.update({'class': "form-control"})

