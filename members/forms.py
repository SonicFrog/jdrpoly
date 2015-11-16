# coding: utf-8

from django.forms import Form, CharField, ChoiceField, EmailField

from .models import Code


class CodeCreationForm(Form):
    email = EmailField()
    semesters = ChoiceField(choices=Code.CHOICES)


class CodeUseForm(Form):
    content = CharField(max_length=30, label=False)

    def is_valid(self):
        if not super(CodeUseForm, self).is_valid():
            return False
        try:
            Code.objects.get(content=self.cleaned_data['content'])
        except:
            return False
        return True
