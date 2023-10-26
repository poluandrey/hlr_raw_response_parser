# Generated by Django 4.2.5 on 2023-10-24 08:28

from django.db import migrations, models
import hlr.parser.hlr_parser


class Migration(migrations.Migration):

    dependencies = [
        ('hlr', '0003_remove_hlrproduct_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='hlrproduct',
            name='type',
            field=models.CharField(choices=[(hlr.parser.hlr_parser.HlrParserType['TMT_HLR'], 1), (hlr.parser.hlr_parser.HlrParserType['INFOBIP_HLR'], 2), (hlr.parser.hlr_parser.HlrParserType['XCONNECT_HLR'], 3), (hlr.parser.hlr_parser.HlrParserType['XCONNECT_MNP'], 4)], default=1),
            preserve_default=False,
        ),
    ]