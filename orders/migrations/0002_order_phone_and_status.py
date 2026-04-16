from django.db import migrations, models


def normalize_pending_status(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.filter(status='penging').update(status='pending')


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=20, verbose_name='Телефон'),
            preserve_default=False,
        ),
        migrations.RunPython(normalize_pending_status, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='order',
            name='full_name',
            field=models.CharField(max_length=200, verbose_name='Получатель'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Ожидает'),
                    ('paid', 'Оплачен'),
                    ('shipped', 'Отправлен'),
                    ('delivered', 'Доставлен'),
                    ('cancelled', 'Отменен'),
                ],
                default='pending',
                max_length=20,
                verbose_name='Статус',
            ),
        ),
    ]
