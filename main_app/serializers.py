from rest_framework import serializers
from .models import Course, StudentEnrollment, CourseStaff, Assignment, Submission, Attendance
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields =  ['id', 'first_name', 'last_name', 'email']


class CourseSerializer(serializers.ModelSerializer):
    # students = 
    # assignments = 
    
    class Meta:
        model = Course
        fields = '__all__'


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        read_only_fields = ['course', 'user']


class CourseStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStaff
        fields = '__all__'
        read_only_fields = ['course', 'user']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['course']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ['student', 'assignment']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['student', 'course']


