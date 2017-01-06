import datetime

from django.test import TestCase
from example.forms import MyModelSearchForm
from example.models import MyModel


class SearchListViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        MyModel.objects.create(
            created=datetime.datetime(2016, 3, 1, 12, 0, 0),
            name="foo",
            birthday=datetime.date(2016, 3, 1),
            number=10,
            status=0,
        )
        MyModel.objects.create(
            created=datetime.datetime(2016, 3, 2, 12, 0, 0),
            name="bar",
            birthday=datetime.date(2016, 3, 2),
            number=11,
            status=1,
        )
        MyModel.objects.create(
            created=datetime.datetime(2016, 3, 3, 12, 0, 0),
            name="baz",
            birthday=datetime.date(2016, 3, 3),
            number=12,
            status=2,
        )
        MyModel.objects.create(
            created=datetime.datetime(2016, 3, 4, 12, 0, 0),
            name="qux",
            birthday=datetime.date(2016, 3, 4),
            number=13,
            status=3,
        )
        MyModel.objects.create(
            created=datetime.datetime(2016, 3, 5, 12, 0, 0),
            name="quux",
            birthday=datetime.date(2016, 3, 5),
            number=14,
            status=4,
        )
        MyModel.objects.create(
            created=datetime.datetime(2016, 3, 5, 12, 0, 0),
            name="foobar",
            birthday=datetime.date(2016, 3, 5),
            number=15,
            status=5,
        )

    def setUp(self):
        self.form = MyModelSearchForm

    def test_blank_data(self):
        form = self.form({})
        self.assertTrue(form.is_valid())
