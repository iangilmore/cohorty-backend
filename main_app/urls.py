from django.urls import path
from .views import Home, Login, VerifyUser, CourseList, CreateCourse, CourseDetail, CourseStaff, StudentEnrollment, AssignmentList, CreateAssignment, AssignmentDetail, StudentList #, StudentDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/login/', Login.as_view(), name='login'),
  path('users/token/refresh/', VerifyUser.as_view(), name='token_refresh'),
  path('courses/', CourseList.as_view(), name='courses'),
  path('course/', CreateCourse.as_view(), name='create_course'),
  path('<int:course_id>/', CourseDetail.as_view(), name='course'),
  path('<int:course_id>/staff/<int:user_id>/', CourseStaff.as_view(), name='course_staff'),
  path('<int:course_id>/student-enrollment/<int:user_id>/', StudentEnrollment.as_view(), name='student_enrollment'),
  path('<int:course_id>/assignments/', AssignmentList.as_view(), name='assignments'),
  path('<int:course_id>/assignment/', CreateAssignment.as_view(), name='create_assignment'),
  path('<int:course_id>/assignment/<int:assignment_id>/', AssignmentDetail.as_view(), name='assignment'),
  path('<int:course_id>/students/', StudentList.as_view(), name='students'),
#  path('<int:course_id>/student/<int:student_enrollment_id>/', StudentDetail.as_view(), name='student'),
  ]