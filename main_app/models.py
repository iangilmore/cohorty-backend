from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
  name = models.CharField(max_length=255)
  
  def __str__(self):
    return self.name


class StudentEnrollment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, related_name='students', on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name}"
  
  def name(self):
    return f"{self.user.first_name} {self.user.last_name}"


class CourseStaff(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name}"
  
  def get_name(self):
    return f"{self.user.first_name} {self.user.last_name}"

class Assignment(models.Model):
  course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  due_date = models.DateField()
  
  def __str__(self):
    return self.name


class Submission(models.Model):
  student = models.ForeignKey(StudentEnrollment, related_name='submissions', on_delete=models.CASCADE)
  assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete= models.CASCADE)
  is_complete = models.BooleanField(default=False)
  
  def __str__(self):
    return f"{self.assignment} from {self.student}"
  
  class Meta:
    unique_together = ('assignment', 'student')



class Attendance(models.Model):
  date = models.DateField()
  student = models.ForeignKey(StudentEnrollment, on_delete=models.CASCADE)
  status = models.CharField(max_length=50, choices=[('Late', 'Late'), ('Absent', 'Absent')])

  class Meta:
    unique_together = ('date', 'student')
  
  def __str__(self):
    return f"{self.student} was {self.status} on {self.date}"
  
  