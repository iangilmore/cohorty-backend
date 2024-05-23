from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import (
    Course,
    Assignment,
    CourseStaff,
    StudentEnrollment,
    Submission,
    Attendance,
)
from .serializers import (
    UserSerializer,
    CourseSerializer,
    CourseStaffSerializer,
    AssignmentListSerializer,
    AssignmentDetailSerializer,
    SubmissionSerializer,
    AttendanceSerializer,
    StudentSerializer,
    StudentDetailSerializer,
)

# from .serializers import UserSerializerWithToken, CourseListSerializer, CourseDetailSerializer, StudentListSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class Home(APIView):
    def get(self, request):
        content = {"message": "Welcome to the Cohorty API"}
        return Response(content)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class VerifyUser(APIView):
    # This ensures that only authenticated users can access this view.
    permission_classes = [permissions.IsAuthenticated]

    # request: Represents the HTTP request received
    def get(self, request):
        # Searches the database for the User object whose username matches request.user
        user = User.objects.get(username=request.user)
        refresh = RefreshToken.for_user(request.user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )


class Courses(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(coursestaff__user=user)


class CourseDetail(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(coursestaff__user=user)


class Staff(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CourseStaff.objects.all()
    serializer_class = CourseStaffSerializer


class Assignments(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentListSerializer
    # lookup_field = "course_id"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        return Assignment.objects.filter(
            course_id=self.kwargs["course_id"], course__coursestaff__user=user
        )
        
    def post(self, request):
        course = self.kwargs["course_id"]
        serializer = AssignmentListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return Assignment.objects.filter(
            course_id=self.kwargs["course_id"], course__coursestaff__user=user
        )

    def put(self, request, *args, **kwargs):
        assignment = self.get_object()
        submissions_data = request.data.get("submissions", [])

        existing_submissions = Submission.objects.filter(assignment=assignment)

        submission_ids = set(
            submission_data.get("id") for submission_data in submissions_data
        )

        for submission in existing_submissions:
            if submission.id not in submission_ids:
                submission.delete()

        for submission_data in submissions_data:
            submission_id = submission_data.get("id")

            if submission_id:
                submission = Submission.objects.filter(id=submission_id).first()

                if submission:
                    serializer = SubmissionSerializer(submission, data=submission_data)

                    if serializer.is_valid():
                        serializer.save()
            else:
                serializer = SubmissionSerializer(data=submission_data)

                if serializer.is_valid():
                    serializer.save(assignment=assignment)

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        assignment = self.get_object()
        assignment.delete()
        return self.destroy(request, *args, **kwargs)


class Students(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        return StudentEnrollment.objects.filter(
            course_id=self.kwargs["course_id"], course__coursestaff__user=user
        )


class StudentDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return StudentEnrollment.objects.filter(
            course_id=self.kwargs["course_id"], course__coursestaff__user=user
        )

    def put(self, request, *args, **kwargs):
        student = self.get_object()
        attendance_data = request.data.get("attendance", [])
        submissions_data = request.data.get("submissions", [])

        existing_attendances = Attendance.objects.filter(student=student)
        existing_submissions = Submission.objects.filter(student=student)

        attendance_ids = set(
            attendance_data.get("id") for attendance_data in attendance_data
        )
        submission_ids = set(
            submission_data.get("id") for submission_data in submissions_data
        )

        for attendance in existing_attendances:
            if attendance.id not in attendance_ids:
                attendance.delete()

        for submission in existing_submissions:
            if submission.id not in submission_ids:
                submission.delete()

        for attendance_data in attendance_data:
            attendance_id = attendance_data.get("id")
            if attendance_id:
                attendance = Attendance.objects.filter(id=attendance_id).first()
                if attendance:
                    serializer = AttendanceSerializer(attendance, data=attendance_data)

                    if serializer.is_valid():
                        serializer.save()
            else:
                serializer = AttendanceSerializer(data=attendance_data)

                if serializer.is_valid():
                    serializer.save(student=student)

        for submission_data in submissions_data:
            submission_id = submission_data.get("id")
            if submission_id:
                submission = Submission.objects.filter(id=submission_id).first()
                if submission:
                    serializer = SubmissionSerializer(submission, data=submission_data)

                    if serializer.is_valid():
                        serializer.save()
            else:
                serializer = SubmissionSerializer(data=submission_data)

                if serializer.is_valid():
                    serializer.save(student=student)

        return self.update(request, *args, **kwargs)
