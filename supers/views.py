from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super
from super_types.models import SuperType
from super_types.serializers import SuperTypeSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def supers_list(request):
    
    if request.method == 'GET':
        # super_types = SuperType.objects.all()
        supertype = request.query_params.get('super_type')
        super = Super.objects.all()
        if supertype:
            supers = super.filter(super_type__type=supertype)
            serializer = SuperSerializer(supers, many=True)
            return Response(serializer.data)
        else:
            heroes = Super.objects.filter(super_type_id = 1)
            heroes_serializer = SuperSerializer(heroes, many=True)
            villians = Super.objects.filter(super_type_id = 2)
            villians_serializer = SuperSerializer(villians, many=True)
            custom_response = {
            "Heroes": heroes_serializer.data,
            "Villians": villians_serializer.data,
        }
        return Response(custom_response)
        
    
    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def supers_detail(request, pk):
     supers = get_object_or_404(Super, pk=pk)
     if request.method == 'GET':
         serializer = SuperSerializer(supers)
         return Response(serializer.data)
     elif request.method == 'PUT':
         serializer = SuperSerializer(supers, data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data)
     elif request.method == 'DELETE':
         supers.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)