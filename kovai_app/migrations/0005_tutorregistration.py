# Generated by Django 4.1.1 on 2024-08-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kovai_app', '0004_remove_tutorrequest_meeting_option_my_place_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('confirm_password', models.CharField(max_length=255)),
                ('types', models.CharField(blank=True, choices=[('individual_teaching', 'Individual Teaching'), ('teaching_company', 'Teaching Company')], max_length=50, null=True)),
                ('strength', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('post_code', models.CharField(blank=True, max_length=20, null=True)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('from_level', models.CharField(blank=True, max_length=255, null=True)),
                ('to_level', models.CharField(blank=True, max_length=255, null=True)),
                ('institution_name', models.CharField(blank=True, max_length=255, null=True)),
                ('degree_type', models.CharField(blank=True, choices=[('Secondary', 'Secondary'), ('Higher_Secondary', 'Higher Secondary'), ('Diploma', 'Diploma'), ('Graduation', 'Graduation'), ('AdvancedDiploma', 'Advanced Diploma'), ('PostGraduation', 'Post Graduation'), ('Doctorate/PhD', 'Doctorate/PhD'), ('Certification', 'Certification'), ('Other', 'Other')], max_length=50, null=True)),
                ('degree_name', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('association', models.CharField(blank=True, choices=[('parttime', 'Part time'), ('fulltime', 'Full time'), ('Correspondence', 'Correspondence / Distance Learning')], max_length=50, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('job_start_date', models.DateField(blank=True, null=True)),
                ('job_end_date', models.DateField(blank=True, null=True)),
                ('job_description', models.TextField(blank=True, null=True)),
                ('i_charge', models.CharField(blank=True, choices=[('per_hour', 'per hour'), ('per_month', 'per month'), ('per_year', 'per year')], max_length=20, null=True)),
                ('min_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_experience', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('teaching_experience', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('online_experience', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('willing_to_travel', models.BooleanField(blank=True, default=False, null=True)),
                ('available_for_online_teaching', models.BooleanField(blank=True, default=False, null=True)),
                ('help_with_homework', models.BooleanField(blank=True, default=False, null=True)),
                ('full_time_teacher', models.BooleanField(blank=True, default=False, null=True)),
                ('interested_in', models.CharField(blank=True, choices=[('online_teaching', 'Online teaching'), ('offline_teaching', 'Offline teaching'), ('full_time', 'Full Time'), ('part_time', 'Part Time'), ('both', 'Both')], max_length=20, null=True)),
                ('profile_description', models.TextField(blank=True, null=True)),
                ('id_proof', models.FileField(blank=True, null=True, upload_to='id_proofs/')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
            ],
        ),
    ]
