from django.db import models

class Classroom(models.Model):
    student_count = models.IntegerField()
    teacher_name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField()
    
    def __str__(self):
        return f"Class with {self.teacher_name} on {self.date}"
