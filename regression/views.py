from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, FileResponse
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
        
        if file_data and file_data.content_type == 'text/csv':
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
                return JsonResponse({"message": "file creation failed"}, status=400)
            
            new_dataset = DatasetPreprocessor(file_path, file_name)
            preprocessed_file_dict = new_dataset.clean_file()
            return JsonResponse({"preprocessSuccess": True,
                                 "fileInfo": preprocessed_file_dict}, status = 201)
            
        else:
            return JsonResponse({"errorMessage": "Invalid Input File"}, status=400)
        
        

@csrf_exempt
def file_download_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file_name = data["fileName"]
            file_path = os.path.join(settings.BASE_DIR, "files", "preprocessed", file_name)
            print(file_path)
            
            # Check if the file exists
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'))
            else:
                return JsonResponse({"errorMessage": "File Not Found"}, status = 404)
        except:
            return JsonResponse({"errorMessage": "Invalid Json Format"})
    else:
        return JsonResponse({"errorMessage": "Unsupported Http method"}, status=400)
