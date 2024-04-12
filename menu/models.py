from django.db import models


# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, default='')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(parent__isnull=True) & models.Q(
                    title__regex=r"^[A-Za-z_0-9]+$")) | models.Q(
                    parent__isnull=False), name='CK_name_parent'),
            models.UniqueConstraint(fields=('title',),
                                    condition=models.Q(parent__isnull=True),
                                    name='unique_title_parent')
        ]

    def __str__(self):
        return f"[{self.pk}] {self.title}"

