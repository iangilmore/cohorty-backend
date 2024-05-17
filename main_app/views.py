from rest_framework.views import APIView
from rest_framework.response import Response

# Define the home vie
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the Cohorty API home route!'}
    return Response(content)