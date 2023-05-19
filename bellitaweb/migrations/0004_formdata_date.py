

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bellitaweb", "0003_remove_formdata_id_alter_formdata_mobile_number"),
    ]
    operations = [
        migrations.AddField(
            model_name='formdata',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
