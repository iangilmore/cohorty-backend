from django.urls import path
from .views import (
    Home,
    Login,
    VerifyUser,
    Courses,
    CourseDetail,
    Staff,
    Assignments,
    AssignmentDetail,
    Students,
    StudentDetail,
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("users/login/", Login.as_view(), name="login"),
    path("users/token/refresh/", VerifyUser.as_view(), name="token_refresh"),
    path("courses/", Courses.as_view(), name="courses"),
    path("courses/<int:id>/", CourseDetail.as_view(), name="course_detail"),
    path(
        "courses/<int:course_id>/staff/",
        Staff.as_view(),
        name="course_staff",
    ),
    path(
        "courses/<int:course_id>/assignments/",
        Assignments.as_view(),
        name="assignments",
    ),
    path(
        "courses/<int:course_id>/assignments/<int:id>/",
        AssignmentDetail.as_view(),
        name="assignment",
    ),
    path("courses/<int:course_id>/students/", Students.as_view(), name="students"),
    path(
        "courses/<int:course_id>/students/<int:id>/",
        StudentDetail.as_view(),
        name="student",
    ),
]
