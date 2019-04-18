from django.db import models
from django.contrib.auth.models import User

class Templates(models.Model):
    template=models.ImageField(upload_to="usertemplates/")
    title=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete = models.CASCADE)

    @property
    def blanks(self):
        return Blanks.objects.filter(templates=self)


class Blanks(models.Model):
    templates=models.ForeignKey(Templates,on_delete=models.CASCADE)
    blank_no=models.CharField(max_length=200)
    start=models.CharField(max_length=200)
    end=models.CharField(max_length=200)

    class Meta:
        unique_together = ('templates', 'blank_no',)

class Csv(models.Model):
    csvfile=models.FileField(upload_to="userfiles/")

    def __str__(self):
        return self.csvfile.name

class Link(models.Model):
    link=models.URLField()
    user=models.ForeignKey(User,on_delete = models.CASCADE)
    template_title=models.CharField(max_length=200)
