import datetime
from haystack import indexes
from xplor.models import *


class ItineraryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    location = indexes.CharField(model_attr='location')
    date = indexes.DateField(model_attr='date')
    tags = indexes.CharField(model_attr='tags')
    description = indexes.CharField(model_attr='description')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Itinerary

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())