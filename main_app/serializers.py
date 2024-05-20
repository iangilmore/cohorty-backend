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

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
        
        
class StudentDetailSerializer(serializers.ModelSerializer):
    user = StudentSerializer()
    assignment_percentage = serializers.SerializerMethodField()
    total_absences = serializers.SerializerMethodField()

    class Meta:
        #because it is the model that represents the student's enrollment in a course
        model = StudentEnrollment
        fields = ['user', 'assignment_percentage', 'total_absences']

    def get_assignment_percentage(self, obj):
        submissions = Submission.objects.filter(student=obj)
        assignments = Assignment.objects.all
        total_assignments = assignments.count()
        completed_assignments = submissions.filter(is_complete=True).count()
        if total_assignments > 0:
            return (completed_assignments / total_assignments) * 100
        return 0

    def get_total_absences(self, obj):
        absences = Attendance.objects.filter(student=obj, status='Absent')
        return absences.count()


