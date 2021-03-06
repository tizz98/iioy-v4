# Generated by Django 2.0.4 on 2018-04-07 20:12

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import iioy.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CastMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('character_name', models.TextField(null=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tmdb_id', models.TextField()),
                ('name', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tmdb_id', models.TextField()),
                ('title', models.TextField()),
                ('original_title', models.TextField()),
                ('slug', iioy.core.fields.SlugField(slug_field='title')),
                ('tagline', models.TextField(null=True)),
                ('budget', models.BigIntegerField(null=True)),
                ('revenue', models.BigIntegerField(null=True)),
                ('homepage', models.URLField(null=True)),
                ('imdb_id', models.TextField()),
                ('synopsis', models.TextField(null=True)),
                ('runtime', models.IntegerField(null=True)),
                ('mpaa_rating', models.TextField(null=True)),
                ('release_date', models.DateField(null=True)),
                ('backdrop_url', models.URLField(null=True)),
                ('mobile_backdrop_url', models.URLField(null=True)),
                ('poster_url', models.URLField(null=True)),
                ('mobile_poster_url', models.URLField(null=True)),
                ('trailer_url', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('source', models.TextField()),
                ('name', models.TextField()),
                ('slug', iioy.core.fields.SlugField(slug_field='name')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('source', models.TextField()),
                ('value', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('tmdb_id', models.TextField()),
                ('name', models.TextField()),
                ('profile_picture_url', models.URLField()),
                ('biography', models.TextField(null=True)),
                ('day_of_birth', models.DateField(null=True)),
                ('day_of_death', models.DateField(null=True)),
                ('homepage', models.URLField(null=True)),
                ('birthplace', models.TextField(null=True)),
                ('aliases', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None)),
            ],
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['tmdb_id'], name='movies_pers_tmdb_id_944488_idx'),
        ),
        migrations.AddField(
            model_name='movierating',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='movielist',
            name='movies',
            field=models.ManyToManyField(to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='similar_movies',
            field=models.ManyToManyField(related_name='_movie_similar_movies_+', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='castmember',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cast_members', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='castmember',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='movies.Person'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['tmdb_id'], name='movies_movi_tmdb_id_0e4cad_idx'),
        ),
        migrations.AddIndex(
            model_name='movie',
            index=models.Index(fields=['imdb_id'], name='movies_movi_imdb_id_d04af4_idx'),
        ),
    ]
