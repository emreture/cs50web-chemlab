from django import forms
from .models import Sample


class SampleForm(forms.ModelForm):
    receipt_date = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'],
                                       widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                                                  attrs={'type': 'datetime-local',
                                                                         'class': 'form-control'}))
    sampling_date = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'], required=False,
                                        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                                                   attrs={'type': 'datetime-local',
                                                                          'class': 'form-control'}))
    report_date = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'], required=False,
                                      widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                                                 attrs={'type': 'datetime-local',
                                                                        'class': 'form-control'}))

    class Meta:
        model = Sample
        fields = ("__all__")
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'sampling_point': forms.TextInput(attrs={'class': 'form-control'})
        }
