from django.db import models

# Create your models here.

class Teacher(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    class Meta:
        db_table = 'teacher'
        ordering = ['id']
        verbose_name = 'TeacherTable'
        verbose_name_plural = verbose_name

class Class(models.Model):
    name = models.CharField(max_length=255)
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class Meta:
        db_table = 'class'
        ordering = ['id']
        verbose_name = 'ClassTable'
        verbose_name_plural = verbose_name

class Student(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    video_watching_counts = models.FloatField()
    video_watching_seconds = models.FloatField()
    course_discuss_related = models.FloatField()
    course_discuss_unrelated = models.FloatField()
    discuss_topic_numbers = models.FloatField()
    discussion_comment_and_reply_numbers = models.FloatField()
    spoc_score = models.FloatField()
    test_mean = models.FloatField()
    cid = models.ForeignKey(Class, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, null=True, blank=True)
    advice = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'student'
        ordering = ['id']
        verbose_name = 'StudentTable'
        verbose_name_plural = verbose_name