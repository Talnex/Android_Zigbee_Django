from django.db import models

# Create your models here.


class Blog(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(default='文章标题', max_length=50)
    author = models.CharField(default="神秘人",max_length=20)
    image = models.ImageField(default='default.png', upload_to='images/')
    text = models.TextField(default='正文')

    def __str__(self):
        return self.title

    def short_text(self):
        return self.text[:100]

    class Meta:
        ordering = ('-id',)


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.id
