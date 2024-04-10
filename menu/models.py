from django.db import models


# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(parent__isnull=True) & models.Q(
                    title__regex=r"[A-Za-z_0-9]+")) | models.Q(
                    parent__isnull=False), name='CK_name_parent')
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title}"
