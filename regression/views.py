from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class Regression_view(View):
    # def get(self, request, *args, **kwargs):
    #     return JsonResponse({"messsage": "get request received"})
    
    def post(self, request, *args, **kwagrs):
        file_data = request.FILES.get("csvFile")
        json_data = request.POST.get("selectedModels")
        model_data = json.loads(json_data)
        print(file_data)
        for data in model_data:
            print(data["name"], data["checked"])
        return JsonResponse({"message": "request received"}, status=201)
