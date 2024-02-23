
from django import forms
from .models import Vehicle,QualityCheck

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type', 'delivery_challan_number', 'purchase_order_number']
        
class QualityCheckForm(forms.ModelForm):
    passed = forms.BooleanField(label='Passed', required=False)
    
    class Meta:
        model = QualityCheck
        fields = ['passed']