from datetime import datetime, timezone
from django.test import TestCase
from .models import *
# Create your tests here.


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        density = TestMethod.objects.create(number="ASTM D4052", name="Density", unit="g/cm³")
        viscosity = TestMethod.objects.create(number="ASTM D445", name="K. Viscosity", unit="mm²/s")
        sulfur_content = TestMethod.objects.create(number="ASTM D2622", name="Sulfur content", unit="ppm")
        flash_point = TestMethod.objects.create(number="ASTM D93", name="Flash point", unit="°C")
        mon = TestMethod.objects.create(number="ASTM D2700", name="Motor octane number", unit="")

        gasoil = Product.objects.create(name="Gasoil")
        gasoline = Product.objects.create(name="Gasoline")
        gasoil.tests.add(density)
        gasoil.tests.add(viscosity)
        gasoil.tests.add(sulfur_content)
        gasoil.tests.add(flash_point)
        gasoline.tests.add(density)
        gasoline.tests.add(sulfur_content)
        gasoline.tests.add(mon)

        astor = Customer.objects.create(name="Astor A.Ş.", address="Planet Earth")
        emek = Customer.objects.create(name="Emek A.Ş.", address="Planet Mars")

        sample1 = Sample.objects.create(number=200001, receipt_date=datetime(2020, 1, 10, 9, 30, tzinfo=timezone.utc),
                                        product=gasoil, customer=astor,
                                        sampling_date=datetime(2020, 1, 5, tzinfo=timezone.utc),
                                        sampling_point="Shore tank 01",
                                        report_date=datetime(2020, 1, 15, tzinfo=timezone.utc))

        sample2 = Sample.objects.create(number=200002, receipt_date=datetime(2020, 1, 10, 9, 30, tzinfo=timezone.utc),
                                        product=gasoline, customer=astor,
                                        sampling_date=datetime(2020, 1, 5, tzinfo=timezone.utc),
                                        sampling_point="Shore tank 02",
                                        report_date=datetime(2020, 1, 15, tzinfo=timezone.utc))

        result1 = Result.objects.create(sample=sample1, test_method=flash_point, result="60.0")

    def test_object_names(self):
        gasoil = Product.objects.get(name="Gasoil")
        expected_product_name = gasoil.name
        self.assertEqual(str(gasoil), expected_product_name)
        test_method = gasoil.tests.get(name="Density")
        expected_test_method_name = f"{test_method.number} {test_method.name}"
        self.assertEqual(str(test_method), expected_test_method_name)
        sample = Sample.objects.get(number=200001)
        expected_sample_name = f"{sample.number} {sample.product} {sample.customer}"
        self.assertEqual(str(sample), expected_sample_name)
        result = Result.objects.get(pk=1)
        expected_result_name = f"{result.sample.number} {result.test_method.name} {result.result} {result.test_method.unit}"
        self.assertEqual(str(result), expected_result_name)

    def test_object_counts(self):
        test_methods = TestMethod.objects
        self.assertEqual(test_methods.count(), 5)
        products = Product.objects
        self.assertEqual(products.count(), 2)
        gasoil_test_methods = Product.objects.get(name="Gasoil").tests
        self.assertEqual(gasoil_test_methods.count(), 4)
        gasoline_test_methods = Product.objects.get(name="Gasoline").tests
        self.assertEqual(gasoline_test_methods.count(), 3)

    def test_customer_samples_count(self):
        astor_samples = Customer.objects.get(name="Astor A.Ş.").samples
        self.assertEqual(astor_samples.count(), 2)
        emek_samples = Customer.objects.get(name="Emek A.Ş.").samples
        self.assertEqual(emek_samples.count(), 0)

