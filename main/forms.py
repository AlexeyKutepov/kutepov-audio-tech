from django import forms


class FeedbackForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.Field(required=False)
    message = forms.CharField(required=True)


class SubscribeForm(forms.Form):
    email = forms.EmailField(required=True)
