from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    id = models.CharField(max_length=30, primary_key=True)
    email = models.CharField(max_length=30)
    version = models.IntegerField() # 0-en 1-cn
    yesterday = models.IntegerField(default=0)
    today = models.IntegerField(default=0)
    latest = models.IntegerField(default=0)

    def __str__(self):
    # 在Python3中使用 def __str__(self):
        return '(' + self.name + ',' + self.id  + ',' + self.email + ')'