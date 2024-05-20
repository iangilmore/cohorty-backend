from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Course, Assignment, CourseStaff, StudentEnrollment, Submission, Attendance
from .serializers import CourseSerializer, AssignmentSerializer, CourseStaffSerializer, StudentEnrollmentSerializer, SubmissionSerializer, AttendanceSerializer, UserSerializer, StudentDetailSerializer
# from .serializers import UserSerializerWithToken, CourseListSerializer, CourseDetailSerializer, StudentListSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
# Define the home vie
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the Cohorty API home route!'}
    return Response(content)
  

# Define the login view

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    
  #VerifyUserView
  
class VerifyUser(APIView):
  #This ensures that only authenticated users can access this view.
  permission_classes = [permissions.IsAuthenticated]
  #request: Represents the HTTP request received
  def get(self, request):
  #Searches the database for the User object whose username matches request.user
     user = User.objects.get(username=request.user)
     refresh = RefreshToken.for_user(request.user)
     return Response({
       'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
     })
    
  #CoursesView
  
  # think we do not need one list and create because list = list and create = create so they do both, they inhere both, get and post 
  
  
class CourseList(generics.ListCreateAPIView):
  # permission_classes = [permissions.IsAuthenticated]
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
    
  
  #CreateCourseView
  
class CreateCourse(generics.CreateAPIView):
  # permission_classes = [permissions.IsAuthenticated]
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  
  #CourseView
  
class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
  # permission_classes = [permissions.IsAuthenticated]
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  
  #CourseStaffView
  
class CourseStaff(generics.ListCreateAPIView):
  # permission_classes = [permissions.IsAuthenticated]
  queryset = Course.objects.all()
  serializer_class = CourseStaffSerializer
  
  #StudentEnrollmentView
class StudentEnrollmentView(generics.ListCreateAPIView):
  # permission_classes = [permissions.IsAuthenticated]
  queryset = Course.objects.all()
  serializer_class = StudentEnrollmentSerializer
 
    
 #AssignmentsView
class AssignmentList(generics.ListCreateAPIView):
  #  permission_classes = [permissions.IsAuthenticated]
   queryset = Course.objects.all()
   serializer_class = AssignmentSerializer
  
 
 #CreateAssignmentView
 
class CreateAssignment(generics.CreateAPIView):
  #  permission_classes = [permissions.IsAuthenticated]
   queryset = Course.objects.all()
   serializer_class = AssignmentSerializer
 
 #AssignmentView
 
class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
  #  permission_classes = [permissions.IsAuthenticated]
   queryset = Course.objects.all()
   serializer_class = AssignmentSerializer
 
 
 #StudentsView
 
class StudentList(generics.ListCreateAPIView):
  #  permission_classes = [permissions.IsAuthenticated]

class StudentDetail(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentDetailSerializer
    lookup_field = 'id'