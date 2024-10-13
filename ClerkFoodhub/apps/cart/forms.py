from django import forms
import datetime
from .models import Orders

username = str(datetime.datetime.now().timestamp())


class OrdersForm(forms.ModelForm):

    class Meta:
        model = Orders
        fields = '__all__'
        # widgets = {
        #     'userName': forms.TextInput(attrs= {'value': username, 'type': "text", 'readonly':'readonly',}),
        # }