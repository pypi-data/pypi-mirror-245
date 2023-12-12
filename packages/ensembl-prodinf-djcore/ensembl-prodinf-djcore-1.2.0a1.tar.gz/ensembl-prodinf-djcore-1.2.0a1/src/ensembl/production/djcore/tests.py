# See the NOTICE file distributed with this work for additional information
#   regarding copyright ownership.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django.test import TestCase
from ensembl.production.djcore.models import BaseTimestampedModel, HasCurrent, HasDescription, NullTextField, \
    TrimmedCharField
from django.db import models, connection
from django.contrib.auth import get_user_model
import random
import string


class DjCoreSampleModel(BaseTimestampedModel, HasCurrent, HasDescription):
    class Meta:
        db_table = "sample"

    foo = models.CharField("Foo Char Field", max_length=255, null=True)
    description = models.TextField("Sample Text", null=True)
    null_field = NullTextField('Null trimmed Text field', null=True)
    trimmed_null_field = NullTextField('Null trimmed Text field', trim_cr=True, null=True)
    carriage = TrimmedCharField("Carriage", max_length=200, null=True)


class TestDjCore(TestCase):
    # TODO add more tests
    user = None
    user2 = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username="testuser")
        cls.user2 = get_user_model().objects.create(username="testuser2")
        return super().setUpTestData()

    def test_timestamped(self):
        bar = DjCoreSampleModel.objects.create(foo="has user", created_by=self.user)
        self.assertTrue(hasattr(bar, 'created_by'))
        self.assertEqual(bar.created_by.username, 'testuser')
        self.assertIsNotNone(bar.created_at)
        bar.foo = "update foobar"
        bar.modified_by = self.user2
        bar.save(update_fields=['foo', 'modified_by'])
        self.assertEqual(bar.modified_by.username, 'testuser2')

    def test_has_description(self):
        bar = DjCoreSampleModel.objects.create(foo="has description", created_by=self.user)
        bar.description = "".join([random.choice(string.ascii_lowercase) for i in range(300)])
        self.assertEqual(len(bar.short_description), 150)
        self.assertEqual(len(bar.description), 300)

    def test_has_current(self):
        bar = DjCoreSampleModel.objects.create(foo="has current", created_by=self.user)
        self.assertTrue(bar.is_current)

    def test_null_text(self):
        bar = DjCoreSampleModel.objects.create(foo="null",
                                               null_field="A very long text with many lines and so on")
        self.assertEqual(bar.null_field, "A very long text with many lines and so on")
        bar.null_field = ''
        bar.save()
        with connection.cursor() as cursor:
            cursor.execute("SELECT null_field FROM sample WHERE foo = %s", [bar.foo])
            row = cursor.fetchone()
            self.assertEqual(None, row[0])
        self.assertEqual(bar.null_field, '')

    def test_trimmed_field(self):
        DjCoreSampleModel.objects.create(foo="carriage",
                                         carriage="A long \r\ntext with \nsome new \n\nlines \rand carriage return")
        bar = DjCoreSampleModel.objects.get(foo="carriage")
        self.assertEqual(bar.carriage, "A long text with some new lines and carriage return")

    def test_trimmed_null_text_field(self):
        DjCoreSampleModel.objects.create(foo="carriage",
                                         null_field="A long \r\ntext with \nsome new \n\nlines \rand "
                                                    "carriage return",
                                         trimmed_null_field="A long \r\ntext with \nsome new \n\nlines \rand "
                                                            "carriage return")
        bar = DjCoreSampleModel.objects.get(foo="carriage")
        self.assertEqual(bar.trimmed_null_field, "A long text with some new lines and carriage return")
        self.assertEqual(bar.null_field, "A long \r\ntext with \nsome new \n\nlines \rand "
                                         "carriage return")
