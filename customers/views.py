from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

##Customer CRUD API
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]  # JWT protected

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['email']        # Exact matches on email if needed
    search_fields = ['name']            # Partial search on name

    ##Overrided the action methods to return custom reponse
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ##pagination 
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if not queryset.exists():
            return Response({"message": "No customers found."}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Successfully fetched all customers.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return Response({"message": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "message": "Customer details fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Customer created successfully.",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "message": "Customer updated successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "message": "Customer partially updated successfully.",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Customer deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

