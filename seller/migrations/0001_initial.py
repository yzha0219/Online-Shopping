# Generated by Django 2.2.3 on 2019-09-03 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user.User')),
                ('status', models.PositiveIntegerField(choices=[{1, 'normal'}, {0, 'deleted'}, {2, 'banned'}, {'VIP', 3}], default=1, verbose_name='status')),
                ('delivery_out_address', models.CharField(db_index=True, max_length=200, verbose_name='delivery_out_address')),
                ('store', models.ManyToManyField(related_name='sellers_stores', to='shop.Store')),
            ],
            bases=('user.user',),
        ),
    ]
