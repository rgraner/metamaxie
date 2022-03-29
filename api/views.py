from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScholarshipModelSerializer
from scholarships.models import Scholarship



@api_view(['GET', 'POST'])
def scholarship_list(request):
    if request.method=='GET':
        qs = Scholarship.objects.all()
        serializer = ScholarshipModelSerializer(qs, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def scholarship(request, ronin_id):
    if request.method=='GET':
        qs = Scholarship.objects.get(id=ronin_id)
        serializer = ScholarshipModelSerializer(qs)
        return Response(serializer.data)
