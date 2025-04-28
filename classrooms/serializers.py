from rest_framework import serializers
from .models import Classroom

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'student_count', 'teacher_name', 'date', 'start_time', 'end_time', 'reason']