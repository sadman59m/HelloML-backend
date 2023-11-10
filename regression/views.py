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
from .mlmodels import LinearRegression


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class Regression_view(View):
    # def get(self, request, *args, **kwargs):
    #     return JsonResponse({"messsage": "get request received"})
    
    def post(self, request, *args, **kwagrs):
        file_data = request.FILES.get("csvFile")
        json_data = request.POST.get("selectedModels")
        model_data = json.loads(json_data)
        
        # get the all models info
        all_models = model_data[0]
        print(all_models)
        selected_models = []
        
        # filter the model name of the selected models
        for modelInfo in all_models:
            if modelInfo['checked'] == True:
                selected_models.append(modelInfo["id"])
                
        print(selected_models)
        print(len(selected_models))
        
        # validating split ratio
        try:
            split_ratio = float(model_data[-1].get('splitRatio'))
            print(split_ratio)
            if split_ratio <= 0.0 or split_ratio >= 1.0:
                raise Exception("Invalid Split Ration")
        except:
            return JsonResponse({"errorMessage": "Invalid Split Ratio.Keep in Range of 0 and 1."}, status = 400)
        
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
            
            # apply Data Preprocessor
            new_dataset = DatasetPreprocessor(file_path, file_name)
            
            #returns a tuple with 1st the 2D array, 2nd success flag True or False
            preprocessed_file_values_tuple = new_dataset.clean_file()
            
            #access the 2nd value to see the success flag. False if preprocessing fails
            if preprocessed_file_values_tuple[1] == False:
                return JsonResponse({"preprocessSuccess": False, 
                                     "errorMessage": """Data Preprocessing Failed. This Dataset is not suitable for our Operations.
                                     Please, try with another dataset accourding to our instructions""",
                                     }, 
                                    status=200)
                
            #convert and get the csv file for this numpy array
            preprocessed_file_values = preprocessed_file_values_tuple[0]
            print(preprocessed_file_values)
            # takes the 2D values and return a dict with filename and filepath
            preprocessed_file_dict = new_dataset.get_preprocessed_csv_file(preprocessed_file_values)
            
            
            # appling dataset to the selected models    
            # if len(selected_models) > 0:
            #     linear_flag = False
            #     polynomial_flag = False
            #     svr_flag = False
            #     dt_flag = False
            #     rmf_flag = False
                
            #     print(selected_models)
            # print(preprocessed_file_dict)
            # linear_regression = LinearRegression(preprocessed_file_dict["filePath"], split_ratio)
            # linear_regression.perform_regression()
                
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
