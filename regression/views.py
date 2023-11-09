from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
import json
import uuid
import os

from .preprocessor import DatasetPreprocessor


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class Regression_view(View):
    # def get(self, request, *args, **kwargs):
    #     return JsonResponse({"messsage": "get request received"})
    
    def post(self, request, *args, **kwagrs):
        file_data = request.FILES.get("csvFile")
        json_data = request.POST.get("selectedModels")
        model_data = json.loads(json_data)
        
        if file_data:
            new_uuid = uuid.uuid4()
            file_name = f"{new_uuid}.csv"
            target_folder = os.path.join(settings.MEDIA_ROOT)
            os.makedirs(target_folder, exist_ok=True)
            file_path = os.path.join(target_folder, file_name)
            try:
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file_data.chunks():
                        destination.write(chunk)
            except:
                return JsonResponse({"message": "file creating failed"}, status=400)
            
            new_dataset = DatasetPreprocessor(file_path, file_name)
            new_dataset.clean_file()
            return JsonResponse({"message": "operation successful"}, status = 201)
            
        else:
            return JsonResponse({"message": "file creating failed"}, status=400)
        
        # return JsonResponse({"message": "file creation successful",
        #                             "file_path": file_path,
        #                             "file_name": file_name},
        #                             status = 201)
        
        return JsonResponse({"message": "request received"}, status=201)
