# I have created this file - sayantan
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics
from scipy.io import loadmat

def index(request):

    return render(request, 'index.html')

    # return HttpResponse("Home")
datamain = None
def range(request):
    if request.method == 'POST':
        file = request.FILES['fileupload']
        mat = loadmat(file)
        mat = {k: v for k, v in mat.items() if k[0] != '_'}
        data = pd.DataFrame({k: pd.Series(i[0] for i in v) for k, v in mat.items()})
        data2 = pd.DataFrame(mat['Time_Adjusted'].reshape(7200, 1))
        data['Time_Adjusted'] = data2
        global datamain
        def datamain():
            return data
        print(data)
    return render(request, 'range.html')
datamain = None
def analyze(request):
    import json
    if request.method == 'POST':
        MEAN = request.POST.get('MEAN','off')
        MEDIAN = request.POST.get('MEDIAN', 'off')
        MODE = request.POST.get('MODE', 'off')
        STDEV = request.POST.get('STDEV', 'off')
        print(STDEV)
        Q1Q3 = request.POST.get('Q1Q3', 'off')
        IQR = request.POST.get('IQR', 'off')




        range_1 = request.POST.get('rangeone')
        range_2 = request.POST.get('rangetwo')
        print(range_1, range_2)
        k=datamain()
        list = [['Time','Data']]
        req_ecg1 = []
        req_ecg2 = []
        req_time = []
        req_data = pd.DataFrame()
        for x in k.index:
            if k['Time_Adjusted'][x] >= float(range_1) and k['Time_Adjusted'][x] <= float(range_2):
                list1 =[]
                req_ecg1.append(k['ECG_1'][x])
                req_ecg2.append(k['ECG_2'][x])
                req_time.append(k['Time_Adjusted'][x])
                list1 = [k['Time_Adjusted'][x],k['ECG_1'][x]]
                list.append(list1)
        req_data['ECG_1'] = req_ecg1
        req_data['ECG_2'] = req_ecg2
        req_data['Time_Adjusted'] = req_time
        mean = 0
        mode = 0
        median = 0
        stddev = 0
        Q1=0
        Q3 = 0
        iqr = 0
        if MEAN == 'on':
            mean = round(sum(req_data['ECG_1']) / len(req_data['ECG_1']), 3)

        if (MODE == "on"):
            mode = round(statistics.mode(req_data['ECG_1']), 3)
        if (MEDIAN=="on"):
            median = round(statistics.median(req_data['ECG_1']), 3)
        if(STDEV =="on"):
            stddev = round(statistics.stdev(req_data['ECG_1']), 3)
        if(Q1Q3=="on"):
            Q1 = round(np.percentile(req_data['ECG_1'], 25, interpolation='midpoint'), 3)
            Q3 = round(np.percentile(req_data['ECG_1'], 75, interpolation='midpoint'), 3)

        if(IQR=="on"):
            iqr = round(Q3 - Q1, 3)


        list = json.dumps(list)

        params = {'mean': mean, 'median': median, 'mode': mode, 'stddev': stddev, 'Qone': Q1, 'Qthree': Q3, 'IQR': iqr, 'list':list}
    return render(request, 'analyze.html',params)

def abe(request):

    return render(request,'ecginfo.html')
def aboutus(request):

    return render(request,'aboutus.html')
