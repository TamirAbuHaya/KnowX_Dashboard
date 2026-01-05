from django.db import models
from django.conf import settings


class CourseBattalion(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    battalion = models.CharField(max_length=20)  # matches choices in accounts, we validate at API layer
    course_num = models.PositiveIntegerField()

    commander = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="commanded_courses",
        help_text="Battalion Commander user"
    )

    class Meta:
        unique_together = ("battalion", "course_num")

    def __str__(self):
        return f"{self.battalion} Course {self.course_num}"
