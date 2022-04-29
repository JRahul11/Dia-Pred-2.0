from django.shortcuts import render, redirect
from django.utils import timezone
from .models import HistoryModel
import joblib
import json


def home(request):
    user = request.user
    if request.user.is_authenticated:
        return render(request, 'main_app/home.html')
    return redirect("login")


def predict(request):
    user = request.user
    if request.user.is_authenticated:
        if request.method == 'POST':
            patient_id = int(request.POST.get("patient_id"))
            patient_name = request.POST.get("patient_name")
            data_list = []
            data_list.append(int(request.POST.get('pregancies')))
            data_list.append(int(request.POST.get('glucose')))
            data_list.append(int(request.POST.get('bp')))
            data_list.append(int(request.POST.get('skin')))
            data_list.append(int(request.POST.get('insulin')))
            data_list.append(float(request.POST.get('bmi')))
            data_list.append(float(request.POST.get('dpf')))
            data_list.append(int(request.POST.get('age')))

            model = joblib.load('static/model/finalrfc.sav')
            result = model.predict([data_list])
            
            # model = tf.keras.models.load_model('static/model/dps-dl-model')
            # result = model.predict([data_list])

            print(result)
            if result == 1:
                resulttext = "Positive"
            else:
                resulttext = "Negative"

            HistoryModel.objects.create(user=user, patient_id=patient_id, patient_name=patient_name, pregancies=data_list[0], glucose=data_list[1], bp=data_list[2], skin=data_list[3], insulin=data_list[4], bmi=data_list[5], dpf=data_list[6], age=data_list[7], result=resulttext, datetime=timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M"))

            context = {
                'result': result,
            }
            return render(request, 'main_app/result.html', context)
        return render(request, 'main_app/predict.html')
    return redirect("login")


def history(request, str=None):
    user = request.user
    if user.is_authenticated:
        empty = False
        if str == None:
            history = HistoryModel.objects.filter(user=user).order_by('-datetime')[:8]
            if not history.exists():
                empty = True
            context = {
                'history': history,
                'empty': empty,
            }
            return render(request, 'main_app/history.html', context)
        elif str == 'id':
            history = HistoryModel.objects.filter(user=user).order_by('patient_id')[:8]
            if not history.exists():
                empty = True
            context = {
                'history': history,
                'empty': empty,
            }
            return render(request, 'main_app/history.html', context)
    return redirect("login")


def about(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'main_app/about.html')
    return redirect("login")

def report(request, patient_id):
    user = request.user
    if user.is_authenticated:
        glucoseList = []
        bmiList = []
        dpfList = []
        bpList = []
        stList = []
        insulinList = []
        dateList = []
        records = HistoryModel.objects.filter(patient_id=patient_id)
        for record in records:
            glucoseList.append(record.glucose)
            bmiList.append(record.bmi)
            dpfList.append(record.dpf)
            bpList.append(record.bp)
            stList.append(record.skin)
            insulinList.append(record.insulin)
            dateList.append(record.datetime)
        context = {
            'glucoseList': json.dumps(glucoseList),
            'bmiList': json.dumps(bmiList),
            'dpfList': json.dumps(dpfList),
            'bpList': json.dumps(bpList),
            'stList': json.dumps(stList),
            'insulinList': json.dumps(insulinList),
            'dateList': json.dumps(dateList),
        }
        return render(request, 'main_app/report.html', context)
    return redirect("login")