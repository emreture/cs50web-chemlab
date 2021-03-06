# Generated by Django 3.0.3 on 2020-03-04 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0002_auto_20200304_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='TestMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('unit', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('receipt_date', models.DateTimeField()),
                ('sampling_date', models.DateTimeField(blank=True, null=True)),
                ('sampling_point', models.CharField(max_length=64)),
                ('report_date', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='customers.Customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='samples.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=16)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='results', to='samples.Sample')),
                ('test_method', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='samples.TestMethod')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='tests',
            field=models.ManyToManyField(related_name='products', to='samples.TestMethod'),
        ),
    ]
