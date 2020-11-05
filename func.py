import csv
import datetime
import sys
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#global var
"""now = datetime.datetime.now()
month = now.month"""


#---------------------------nutrient conv function----------------------------#
def conv(nutrient):
    nutrient_dict={'VL':1,'L':2,'M':3,'H':4,'VH':5 }
    return  nutrient_dict.__getitem__(nutrient)
#-----------------------------------------------------------------------------#


#------------areas temp and rain function acc to users month------------------#
def rainfall(temp_final,rainfall_final,temp,rain_fall,month):
    print("inside rainfall")
    print(month,"is the selected month")
    index = int(month)-1
    prevtemp=0
    prevrainfall=0
    for i in range (1,13):
        #print prev
        prevtemp=prevtemp+temp[index]
        temp_final.append(round((prevtemp/i),2))
        prevrainfall=prevrainfall+rain_fall[index]
        rainfall_final.append(round(prevrainfall,2))
        index=index+1
        if index==12:
            index=0



# -------------------get nutrients of farmers area-----------------------------#
def nutrients(state, rainfall_final, temp_final):
    print("inside nutrients")
    try:
        # print('this is state:'+state)
        with open('static/nutrientsarea.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == state:
                    narea = conv(row[1])
                    parea = conv(row[2])
                    karea = conv(row[3])
                    ph = row[4]
    except IOError:
        print("No file exists named nutrientsarea.csv")
        sys.exit("The required file does not exist!!!")
    csvfile.close()

    # nutrient based filter of crops
    try:

        with open('static/cropDB.csv', 'r') as csvfile, open('static/metacrops.csv', 'w') as metacrops:
            reader = csv.reader(csvfile)
            # writer=csv.writer(metacrops)
            metacrops.writelines("Crop, Rainfall, Temperature, pH \n")
            for row in reader:
                ncrop = conv(row[8])
                pcrop = conv(row[9])
                kcrop = conv(row[10])
                if (narea >= ncrop and parea >= pcrop and karea >= kcrop):
                    # swriter.writerows(row)
                    no_months = int(row[1])
                    # print("this in no months",no_months)
                    total = row[0] + "," + str(rainfall_final[no_months - 1]) + "," + str(
                        temp_final[no_months - 1]) + "," + ph + "\n"
                    metacrops.writelines(total)
                    #print(total)
    except IOError:
        print("No file exists named cropDB.csv")
        sys.exit("The required file does not exist!!!")
    csvfile.close()
    metacrops.close()


# -----------------------------------------------------------------------------#
#--------------------replicate file with headings--------------------------------#
def filewrite():
    n=1
    try:
        with open("static/metacrops.csv",'r') as f:
            with open("static/metacrops11.csv", "w") as f1:
                for line in f:
                    if n==1:
                        n=n+1
                        continue
                    f1.write(line)
        print("File write done!!")
    except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            sys.exit("No such file exists")
    f.close()
    f1.close()
#-----------------------------------------------------------------------------#
# ------------------------------sorting fn-------------------------------------#
def quicksort(crop_name, crop_Y_pred, start, end):
    if start < end:
        # partition the list
        pivot = partition(crop_name, crop_Y_pred, start, end)
        # sort both halves
        quicksort(crop_name, crop_Y_pred, start, pivot - 1)
        quicksort(crop_name, crop_Y_pred, pivot + 1, end)
    return crop_name


# partition function
def partition(crop_name, crop_Y_pred, start, end):
    pivot = crop_Y_pred[start]
    left = start + 1
    right = end
    done = False
    while not done:
        while left <= right and crop_Y_pred[left] >= pivot:
            left = left + 1
        while crop_Y_pred[right] <= pivot and right >= left:
            right = right - 1
        if right < left:
            done = True
        else:
            # swap places Y_pred
            temp = crop_Y_pred[left]
            crop_Y_pred[left] = crop_Y_pred[right]
            crop_Y_pred[right] = temp

            # swap places Y_crop
            temp1 = crop_name[left]
            crop_name[left] = crop_name[right]
            crop_name[right] = temp1

    # swap start with myList[right]
    temp = crop_Y_pred[start]
    crop_Y_pred[start] = crop_Y_pred[right]
    crop_Y_pred[right] = temp

    # swap start with myList[right] for crop
    temp1 = crop_name[start]
    crop_name[start] = crop_name[right]
    crop_name[right] = temp1

    return right


# -----------------------------------------------------------------------------#

# ------------------------------MLR function-----------------------------------#
def regression():
    print("Performing regression...")
    # Data Preprocessing
    n = 0
    crop_Y_pred = []
    crop_name = []
    dataset = pd.read_csv('static/regressiondb.csv')
    locbased = pd.read_csv('static/metacrops.csv')
    try:
        with open('static/metacrops11.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # metacrops.writelines("Crop,Production\n")
            # os.remove('final.txt')
            for row in reader:
                crop = row[0]
                # Importing the dataset
                metadata = dataset.loc[dataset['Crop'] == crop]
                X = metadata.iloc[:, :-2].values
                Y = metadata.iloc[:, 4].values
                ##fitting MLR to training set
                ##regressor = LinearRegression()
                ##regressor.fit(X, Y)
                X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
                regressor = LinearRegression()
                regressor.fit(X_train, Y_train)
                # predecting test set results
                '''Y_pred_test = regressor.predict(X_test)
                print("this is Y test:", Y_test)
                print "\n"
                print("this is Y predicted:", Y_pred_test) '''
                # predecting final set results
                X_locbased = locbased.loc[[n]].values  # take all except 0th col that is crop name
                X_locbased = X_locbased[:, 1:4]
                Y_pred = regressor.predict(X_locbased)
                if Y_pred > 0:
                    crop_Y_pred.append(round(Y_pred[0], 3))
                    crop_name.append(crop)
        # print(crop_name,crop_Y_pred)
        sorted_crops = quicksort(crop_name, crop_Y_pred, 0, len(crop_Y_pred) - 1)
        csvfile.close()
        # return pred_crop
        return sorted_crops
    except IOError:
        print("No file exists named metacrops11.csv")
        sys.exit("No such file exists !!")
    os.remove('static/metacrops.csv')
    print("file removed")
    os.remove('static/metacrops11.csv')
    print("file2sss removed")
# -----------------------------------------------------------------------------#

# -----------------------conv crop list to string------------------------------#
def ListtoStr(sorted_crop):
    pred_crop = ""
    comma_flag = 0
    no = len(sorted_crop)
    if (no > 10):
        no = 10
    for i in range(no):
        if comma_flag == 1:
            pred_crop = pred_crop + ","

        pred_crop = pred_crop + sorted_crop[i]
        comma_flag = 1
    return pred_crop


# -----------------------------------------------------------------------------#
# MAIN FUNCTION
def f(area,m):
    month = m
    temp = []
    temp_final = []
    rain_fall = []
    rainfall_final = []
    prevtemp = 0
    prevrainfall = 0

    with open("static/temprainfall.csv") as csvfile:
        print('this is area:'+area)
        reader = csv.reader(csvfile)
        flag = 0
        print("i m  here")

        for row in reader:
            #if area in row:
            if row[0] in row:
                a = row[0]
                if area in a:
                    print("true")
                    print(row)
                    if flag == 0:
                        state = row[1]
                        flag = 1
                    temperature = (float(row[3]) + float(row[4])) / 2
                    temp.append(round(temperature, 2))
                    rain_fall.append(float(row[5]))

    csvfile.close()
    rainfall(temp_final, rainfall_final, temp, rain_fall,month)
    nutrients(state, rainfall_final, temp_final)
    filewrite()
    sorted_crop = regression()
    final_crop = ListtoStr(sorted_crop)
    print("Predicted crops are:")
    print(final_crop)
    return final_crop

