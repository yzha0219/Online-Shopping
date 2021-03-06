# Generated by Django 2.2.6 on 2019-10-23 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(editable=False, verbose_name='comment_content')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('belongproduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwhichproduct', to='product.Product', verbose_name='itemscomments')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whoscomments', to='user.User', verbose_name='comment_owner')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_replies', to='comment.Comment', verbose_name='parent_comment')),
            ],
            options={
                'verbose_name': 'comments',
                'ordering': ('created',),
            },
        ),
    ]
