from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='auther',
            new_name='author',
        ),
    ]
