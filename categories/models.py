from django.db import models

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.TextField(max_length=50, default="null")
    name = models.TextField(max_length=50, default="null", unique=True)
    lft = models.IntegerField()
    rgt = models.IntegerField()

    def __str__(self):
        return str(self.id)

    @classmethod
    def create(cls, parent, name, lft, rgt):
        category = cls(parent=parent, name=name, lft=lft, rgt=rgt)
        return category