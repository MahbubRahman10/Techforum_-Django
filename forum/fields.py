from functools import partial
from itertools import groupby
from operator import attrgetter

from django.forms.models import ModelChoiceIterator, ModelChoiceField




class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
    	return obj.name