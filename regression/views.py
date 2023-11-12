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
from .mlmodels import (LinearRegressionClass, 
                       SupportVectorRegressorClass,
                       DecisionTreeRegressorClass,
                       RandomForestRegressorClass)


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
        selected_model_ids = []
        
        # filter the model name of the selected models
        for modelInfo in all_models:
            if modelInfo['checked'] == True:
                selected_model_ids.append(modelInfo["id"])
        
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
            # print(preprocessed_file_values)
            # takes the 2D values and return a dict with filename and filepath
            preprocessed_file_dict = new_dataset.get_preprocessed_csv_file(preprocessed_file_values)
            
            if preprocessed_file_dict == False:
                return JsonResponse({"preprocessSuccess": False, 
                                     "errorMessage": """Data Preprocessing Failed. This Dataset is not suitable for our Operations.
                                     Please, try with another dataset accourding to our instructions""",
                                     }, 
                                    status=200)
            
            """Creationg an impty dictonary for storing models R2 scores"""
            models_r2_scores = {}
            
            """Creating a model list for all the regression models"""
            regression_models_classes = [(LinearRegressionClass, 'Linear Regression'),
                                         (SupportVectorRegressorClass, 'Support Vector Regression'),
                                         (DecisionTreeRegressorClass, 'Decision Tree Regression'),
                                         (RandomForestRegressorClass, 'Random Forest Regression')]
            
            """Using loop to use selected model IDs as index to selec model classes"""
            for index in range(len(selected_model_ids)):
                regression_model_class = regression_models_classes[index][0]
                regression_model_name = regression_models_classes[index][1]
                """Pass the 2D numpy array values and the split ratio"""
                regression_model_instance = regression_model_class(preprocessed_file_values, split_ratio)
                model_r2_score = regression_model_instance.perform_regression()
                models_r2_scores[regression_model_name] = model_r2_score
            
            
            return JsonResponse({"preprocessSuccess": True,
                                    "fileInfo": preprocessed_file_dict,
                                    "model_results": models_r2_scores,
                                    "split_ration": split_ratio,
                                    }, status = 201)
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
