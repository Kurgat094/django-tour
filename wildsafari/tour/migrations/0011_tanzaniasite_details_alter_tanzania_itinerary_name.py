# Generated by Django 4.2.16 on 2025-03-06 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tour", "0010_tanzania_itinerary"),
    ]

    operations = [
        migrations.AddField(
            model_name="tanzaniasite",
            name="details",
            field=models.TextField(default="No details available"),
        ),
        migrations.AlterField(
            model_name="tanzania_itinerary",
            name="name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Tz_itinerary",
                to="tour.tanzaniasite",
            ),
        ),
    ]
