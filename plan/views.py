from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from plan.models import Plan
from plan.serializers import PlanSerializer


# Create your views here.

class HomeView(APIView):
    def get(self, request):
        return Response(data={'message': 'Welcome back!'})

class PlanListCreateView(APIView):
    """
    This api view is used to get all plans or post new plan
    """
    serializer_class = PlanSerializer
    def get(self,request):
        all_plans = Plan.objects.all()
        srz_data = self.serializer_class(instance=all_plans, many=True).data
        return Response(data=srz_data)

    def post(self,request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class PlanUpdateDeleteView(APIView):
    """
    This api view is used to update or delete plan,
    need authentication for doing operations
    """
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated,]

    def put(self, request, id):
        plan = Plan.objects.get(pk=id)
        srz_data = self.serializer_class(instance=plan, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        plan = Plan.objects.get(pk=id)
        plan.delete()
        return Response(data={'message' : 'plan deleted'},status=status.HTTP_204_NO_CONTENT)