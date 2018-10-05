from django import forms
from .models import Site
from django.conf import settings
import json
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.template.loader import render_to_string

class PayForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('imp_uid',)

    def as_iamport(self):
        hidden_fields = mark_safe(''.join(smart_text(field) for field in self.hidden_fields()))
        fields = {
            'merchant_uid' : str(self.instance.merchant_uid),
            'name': self.instance.name,
            'amount': 9000,
        }
        return hidden_fields + render_to_string('Site/_iamport.html',{
            'json_fields': mark_safe(json.dumps(fields, ensure_ascii=False)),
            'iamport_shop_id':settings.IAMPORT_SHOP_ID,
        })