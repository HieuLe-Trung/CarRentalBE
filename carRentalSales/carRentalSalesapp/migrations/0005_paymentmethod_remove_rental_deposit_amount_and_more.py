# Generated by Django 5.0.7 on 2024-08-09 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carRentalSalesapp', '0004_remove_image_car_remove_rental_mileage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='rental',
            name='deposit_amount',
        ),
        migrations.RemoveField(
            model_name='salecar',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='salecar',
            name='status',
        ),
        migrations.AddField(
            model_name='rental',
            name='actual_return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rental',
            name='confirmation_status',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='rental',
            name='late_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='salecar',
            name='sold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deposit_payment_status', models.CharField(max_length=20)),
                ('rental', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carRentalSalesapp.rental')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carRentalSalesapp.salecar')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(max_length=20)),
                ('rental', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carRentalSalesapp.rental')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='carRentalSalesapp.paymentmethod')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
    ]
