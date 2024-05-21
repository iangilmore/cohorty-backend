from django.urls import path
from .views import Home, Login, VerifyUser, CourseList, CreateCourse, CourseDetail, CourseStaff, StudentEnrollmentView, AssignmentList, CreateAssignment, AssignmentDetail, StudentList,StudentDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/login/', Login.as_view(), name='login'),
  path('users/token/refresh/', VerifyUser.as_view(), name='token_refresh'),
  path('courses/', CourseList.as_view(), name='courses'),
  path('course/', CreateCourse.as_view(), name='create_course'),
  path('<int:id>/', CourseDetail.as_view(), name='course_detail'),
  path('<int:course_id>/staff/<int:user_id>/', CourseStaff.as_view(), name='course_staff'),
  path('<int:course_id>/student-enrollment/<int:user_id>/', StudentEnrollmentView.as_view(), name='student_enrollment'),
  path('<int:id>/assignments/', AssignmentList.as_view(), name='assignments'),
  path('<int:id>/assignment/', CreateAssignment.as_view(), name='create_assignment'),
  path('<int:course_id>/assignment/<int:id>/', AssignmentDetail.as_view(), name='assignment'),
  path('<int:id>/students/', StudentList.as_view(), name='students'),
  path('<int:course_id>/student/<int:id>/', StudentDetail.as_view(), name='student'),
  ]
