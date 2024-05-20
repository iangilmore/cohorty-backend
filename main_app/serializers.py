from rest_framework import serializers
from .models import Course, StudentEnrollment, CourseStaff, Assignment, Submission, Attendance
from django.contrib.auth.models import User 
from datetime import date

class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
    
	class Meta:
		model = User
		fields =  ['id', 'first_name', 'last_name', 'email']


class StudentSerializer(serializers.ModelSerializer):
  name = serializers.SerializerMethodField()
  assignment_percentage = serializers.SerializerMethodField()
  absences = serializers.SerializerMethodField()
  class Meta:
    model = StudentEnrollment
    fields = ['id', 'name', 'assignment_percentage', 'absences']
		
  def get_name(self, obj):
    return obj.name()
  
  def get_assignment_percentage(self, obj):
    submissions = Submission.objects.filter(student=obj)
    assignments = Assignment.objects.all()
    total_assignments = assignments.filter(due_date__lt=date.today()).count()
    completed_assignments = submissions.filter(is_complete=True).count()
    if total_assignments > 0:
      return (completed_assignments / total_assignments) * 100
    return 0
  
  def get_absences(self, obj):
    absences = Attendance.objects.filter(student=obj, status='Absent')
    lates = Attendance.objects.filter(student=obj, status='Late')
    total = round(absences.count() * 1 + lates.count() * 0.333, 2)
    return total


class AssignmentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Assignment
		fields = ['id', 'name', 'due_date']


class CourseSerializer(serializers.ModelSerializer):
	students = StudentSerializer(many=True, read_only=True)
	assignments = AssignmentListSerializer(many=True, read_only=True)
	
	class Meta:
		model = Course
		fields = ['id', 'name', 'students', 'assignments']

class SubmissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Submission
    fields = '__all__'
    read_only_fields = ['student', 'assignment']


class AssignmentDetailSerializer(serializers.ModelSerializer):
  submissions = SubmissionSerializer(many=True, read_only=True)
  class Meta:
    model = Assignment
    fields = ['id', 'name', 'due_date', 'submissions']

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


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['student', 'course']
