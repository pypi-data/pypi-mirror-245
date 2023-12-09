
__version__ = "0.0.1"
def run_all(dataset, predict, actual, group):
    print("Calculating All")
    print("Calculating Statistical/Demographic Parity")
    stat_demo_parity(dataset, predict, group)
    print("==============================================\n")
    print("Calculating Disparate Impact")
    disparate_impact(dataset, predict, group)
    print("==============================================\n")
    print("Calculating Equal Opportunity")
    equal_opportunity(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Equalized Odds")
    equalized_odds(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Overall Accuracy Equality")
    overall_accuracy_equality(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Conditional Use Accuracy Equality")
    conditional_use_accuracy_equality(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Treatment Equality")
    treatment_equality(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Equalizing Disincentives")
    equalizing_disincentives(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Differences in Squared Error")
    differences_in_squared_error(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Balance between Subgroups")
    balance_btwn_subgroups(dataset, predict, actual, group)
    print("==============================================\n")

def run_all_classification(dataset, predict, actual, group):
    print("Calculating All Classification")
    print("Calculating Statistical/Demographic Parity")
    stat_demo_parity(dataset, predict, group)
    print("==============================================\n")
    print("Calculating Disparate Impact")
    disparate_impact(dataset, predict, group)
    print("==============================================\n")
    print("Calculating Equal Opportunity")
    equal_opportunity(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Equalized Odds")
    equalized_odds(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Overall Accuracy Equality")
    overall_accuracy_equality(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Conditional Use Accuracy Equality")
    conditional_use_accuracy_equality(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Treatment Equality")
    treatment_equality(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Equalizing Disincentives")
    equalizing_disincentives(dataset, predict, actual, group)
    print("==============================================\n")
def run_all_regression(dataset, predict, actual, group):
    print("Calculating All Regression")
    print("Calculating Differences in Squared Error")
    differences_in_squared_error(dataset, predict, actual, group)
    print("==============================================\n")
    print("Calculating Balance between Subgroups")
    balance_btwn_subgroups(dataset, predict, actual, group)
    print("==============================================\n")

def determineMulticlass(df, pred_val=None, actual_val=None, group=None):
    """
    determines multiclass fairness metric
    :param df: dataframe
    :param pred_val: predicted value
    :param actual_val: actual value
    :param group: group value
    :return:
    """
    if pred_val is None:
        pred_val = input("Input predicted attribute\n")
    if actual_val is None:
        actual_val = input("Input actual attribute\n")
    if group is None:
        group = input("Input group attribute\n")

    # initiate the variables
    rateDict = dict()
    # values is a list of unique actual values
    values = sorted(list(set(df[actual_val])))
    print(values)

    # loop through each row of the dataframe looking at pred value, actual value, and the group its in
    for pred_x, act_x, group_x in zip(df[pred_val], df[actual_val], df[group]):
        # if the group isnt in the dict
        if group_x not in rateDict:
            # create new dictionary key and set the value to a list of zeros thats the length of values
            rateDict[group_x] = [[0] * len(values) for _ in range(len(values))]
            rateDict[group_x][values.index(pred_x)][values.index(act_x)] += 1
            # print(rateDict)
        else:
            #
            rateDict[group_x][values.index(pred_x)][values.index(act_x)] += 1
    print(rateDict)
    return rateDict


def determineProbabilityRates(df, pred_val=None, actual_val=None, group=None, positive=None):
    """
    determines TPR, FPR, TNR, FNR
    :return: dictionary
    """
    if pred_val is None:
        pred_val = input("Input predicted attribute\n")
    if actual_val is None:
        actual_val = input("Input actual attribute\n")
    if group is None:
        group = input("Input group attribute\n")
    # [TPR, FPR, TNR, FNR]
    # intializes dictionary rateDict
    rateDict = dict()

    for pred_x, actual_x, group_x in zip(df[pred_val], df[actual_val], df[group]):
        if group_x not in rateDict:
            rateDict[group_x] = [0, 0, 0, 0, 0]  # [TPR, TNR, FPR, FNR, total]
        # TRUE
        if pred_x == actual_x:
            # POSITIVE - TRUE POSITIVE RATE
            if str(pred_x) in positive:
                rateDict[group_x] = [rateDict[group_x][0] + 1, rateDict[group_x][1], rateDict[group_x][2],
                                     rateDict[group_x][3], rateDict[group_x][4] + 1]  # TPR
            # NEGATIVE - TRUE NEGATIVE RATE
            else:
                rateDict[group_x] = [rateDict[group_x][0], rateDict[group_x][1], rateDict[group_x][2] + 1,
                                     rateDict[group_x][3], rateDict[group_x][4] + 1]  # TNR
        # FALSE
        else:
            # POSITIVE - FALSE POSITIVE RATE
            if str(pred_x) in positive:
                rateDict[group_x] = [rateDict[group_x][0], rateDict[group_x][1] + 1, rateDict[group_x][2],
                                     rateDict[group_x][3], rateDict[group_x][4] + 1]  # FPR
            # NEGATIVE - FALSE NEGATIVE RATE
            else:
                rateDict[group_x] = [rateDict[group_x][0], rateDict[group_x][1], rateDict[group_x][2],
                                     rateDict[group_x][3] + 1, rateDict[group_x][4] + 1]  # FNR
    # print(rateDict) {2: [15, 0, 8, 1, 24], 3: [15, 1, 4, 0, 20], 4: [34, 0, 11, 1, 46], 1: [5, 0, 3, 0, 8]}
    for x in rateDict:
        #TPR=TP/(TP+FN)
        rateDict[x][0] = rateDict[x][0] / (rateDict[x][0] + rateDict[x][3])
        #FPR=FP/(FP+TN)
        rateDict[x][1] = rateDict[x][1] / rateDict[x][1] + rateDict[x][2]
        #TNR=TN/(FP+TN)
        rateDict[x][2] = rateDict[x][1] / rateDict[x][1] + rateDict[x][2]
        #FNR=FN/(TP+FN)
        rateDict[x][3] = rateDict[x][0] / (rateDict[x][0] + rateDict[x][3])
        del rateDict[x][4]
    print("Ratedict:", rateDict)
    return rateDict


def equal_opportunity(df, pred_val=None, actual_val=None, group=None):
    '''
    determines equal opportunity fairness metric
    :param df: dataframe
    :param rates: determined rates
    :param pred_val: predicted value
    :param actual_val: actual value
    :param group: group value
    :return: the result of equal opporunity fairness - specifically in relation to tpr
    '''
    rates = determineProbabilityRates(df, pred_val, actual_val, group)
    # choices = input("List the group names you'd like to assess (comma separated) or 'all' to assess all")
    # if choices.lower() == "all":
    print("Rates:")
    print(rates)
    # get the list of tprs from rates
    listOfTPR = []
    for x in rates:
        listOfTPR.append(rates[x][0])

    # print(list(combinations(listOfTPR, 2)))
    # determines 4/5th rule
    print("4/5ths rule for TPR:")
    minVal = min(listOfTPR)
    maxVal = max(listOfTPR)
    result = fourFifths(minVal, maxVal)
    # prints result
    if result:
        print("Equal Opportunity: Passed!")
    else:
        print("Equal Opportunity: Failed!")
    return result


def equalized_odds(df, pred_val=None, actual_val=None, group=None):
    '''
    determine equalized odds
    :param df: dataframe
    :param pred_val: predicted value
    :param actual_val: actual value
    :param group: group value
    :return: none
    '''
    # determine rates
    rates = determineProbabilityRates(df, pred_val, actual_val, group)
    # determine tpr
    TPR = equal_opportunity(df, pred_val, actual_val, group)
    # get fpr from rates
    listOfFPR = []
    for x in rates:
        listOfFPR.append(rates[x][1])
    # print("listoffpr:", listOfFPR)
    print("4/5ths rule for FPR:")
    minVal = min(listOfFPR)
    maxVal = max(listOfFPR)
    # print(minVal, maxVal)
    # print(min(listOfFPR), max(listOfFPR))
    FPR = fourFifths(minVal, maxVal)

    # do fourth fifths rule and print output
    if FPR and TPR:
        print("Both are true, therefore\n Equalized Odds: Passed\n")
        return True
    else:
        print("One or both are false, therefore\n Equalized Odds: Failed\n")
        return False


def overall_accuracy_equality(df, pred_val=None, actual_val=None, group=None):
    '''
    determine overall accuracy equality metric
    :param df: dataframe
    :param pred_val: predicted value
    :param actual_val: actual value
    :param group: group value
    :return: none
    '''
    # get rates
    rates = determineMulticlass(df, pred_val, actual_val, group)
    # print(rates)
    # create dictionary
    dictOfTPRTNR = dict()
    # print(type(rates))
    # look at the rates items
    for key, value in rates.items():
        # print(key, value)
        for i in range(len(value)):
            for j in range(len(value[i])):
                # creation of the n-by-n matrix
                if key not in dictOfTPRTNR:
                    # index 0 is sum when act and pred are equal, index 1 is total sum
                    dictOfTPRTNR[key] = [0, 0]
                if i == j:
                    # if i = j then pred = act and the values are added and added to total
                    dictOfTPRTNR[key] = [dictOfTPRTNR[key][0] + value[i][j], dictOfTPRTNR[key][1] + value[i][j]]
                else:
                    # else add just to total
                    dictOfTPRTNR[key] = [dictOfTPRTNR[key][0], dictOfTPRTNR[key][1] + value[i][j]]
                # print(key, dictOfTPRTNR[key])
        # divide sum by total to get percentage for each group
        dictOfTPRTNR[key] = dictOfTPRTNR[key][0] / dictOfTPRTNR[key][1]
    print(dictOfTPRTNR)
    listOfTPRTNR = []
    # just look at values to compare and do 4/5ths rule
    for key, value in dictOfTPRTNR.items():
        listOfTPRTNR.append(value)
    minVal = min(listOfTPRTNR)
    maxVal = max(listOfTPRTNR)
    print(minVal, maxVal)
    result = fourFifths(minVal, maxVal)
    # print result
    if result:
        print("Overall Accuracy Equality: Passed!")
    else:
        print("Overall Accuracy Equality: Failed!")
    return result


def conditional_use_accuracy_equality(df, pred_val=None, actual_val=None, group=None):
    '''
        determine conditional use accuracy equality metric
        :param df: dataframe
        :param pred_val: predicted value
        :param actual_val: actual value
        :param group: group value
        :return: none
    '''
    rates = determineMulticlass(df, pred_val, actual_val, group)
    # print(len(rates))
    dictOfTR = dict()
    listLength = len(set(df[actual_val]))
    # print(type(rates))
    # creation of n-by-n matrix and determine true rates
    for key, value in rates.items():
        for i in range(len(value)):
            for j in range(len(value[i])):
                if key not in dictOfTR:
                    # initilize value of key to a bunch of zeros, example below
                    dictOfTR[key] = [0] * (listLength + 1)  # ex: [A/A, B/B, C/C, D/D, F/F, TOTAL]
                    # print(dictOfTR)
                if i == j:
                    # if i equals j, increment one for act = pred
                    dictOfTR[key][j] = value[i][j]
                # add value to total
                dictOfTR[key][-1] += value[i][j]
    # print(dictOfTR)
    listOfTR = []
    # iterate through true rates
    for key, value in dictOfTR.items():
        for x in range(len(value)):
            # convert to percentages by dividing by total
            dictOfTR[key][x] = dictOfTR[key][x] / dictOfTR[key][-1]
        listOfTR.append(value)
    print(listOfTR)
    comparedList = []
    for i in range(listLength):
        for x in listOfTR:
            comparedList.append(x[i])
        # do four fifths on each true rate (ex: look at all the different A/A, B/B, C/C, etc.
        minVal = min(comparedList)
        maxVal = max(comparedList)
        # print(minVal, maxVal)
        result = fourFifths(minVal, maxVal)
        if not result:
            break
    # print results
    if result:
        print("Conditional Use Accuracy Equality: Passed!")
    else:
        print("Conditional Use Accuracy Equality: Failed!")
    return result


def treatment_equality(df, pred_val=None, actual_val=None, group=None):
    ''''
        determine treatment equality metric, if fnr is 0, metric cant be used
        :param df: dataframe
        :param pred_val: predicted value
        :param actual_val: actual value
        :param group: group value
        :return: none
    '''
    # determine rates
    rates = determineProbabilityRates(df, pred_val, actual_val, group)
    listOfFPRFNR = []
    print(rates)
    for x in rates:
        if (rates[x][1] == 0):
            print("FPR", rates[x][1], "equals zero so cannot have a true comparison")
            listOfFPRFNR = None
            break
        elif (rates[x][3] == 0):
            print("FNR", rates[x][3], "equals zero so cannot have a true comparison")
            listOfFPRFNR = None
            break
        else:
            # fpr/fnr
            listOfFPRFNR.append(rates[x][1] / rates[x][3])
    if listOfFPRFNR is not None:
        minVal = min(listOfFPRFNR)
        maxVal = max(listOfFPRFNR)
        # print(listOfFPRFNR)
        # do fourth fifths rule and print output
        result = fourFifths(minVal, maxVal)
        if result:
            print("Treatment Equality: Success!")
        else:
            print("Treatment Equality: Failed!")
    else:
        print("cant be done")
        result = None
    return result


def equalizing_disincentives(df, pred_val=None, actual_val=None, group=None):
    '''
        Calculates Equalizing Disincentives metric on trained dataset
        :param df: trained data from user
        :return: None, prints if data successfully passed or failed the metric
    '''
    # determine rate
    rates = determineProbabilityRates(df, pred_val, actual_val, group)
    listOfTPRFPR = []
    # tpr - fpr
    for x in rates:
        listOfTPRFPR.append(rates[x][0] - rates[x][1])
    minVal = min(listOfTPRFPR)
    maxVal = max(listOfTPRFPR)
    print(listOfTPRFPR)
    # do fourth fifths rule and print output
    result = fourFifths(minVal, maxVal)
    if result:
        print("Equalizing Disincentives: Passed!")
    else:
        print("Equalizing Disincentives: Failed!")
    return result


def fourFifths(minVal, maxVal):
    '''
    calculates the four fifths rule
    :param minVal: minimum value of calculated data
    :param maxVal: maximum value of calculated data
    :return:
    '''
    # multiply maxVal by 4/5 and if that calculated value is less than or equal to the min value, it passes, otherwise it fails
    fourFifthsMax = maxVal * (4 / 5)
    if minVal >= fourFifthsMax:
        print(minVal, "is greater than or equal to", fourFifthsMax, "therefore it passes the fourth fifths rule")
        return True
    else:
        print(minVal, "is less than", fourFifthsMax, "therefore it fails the fourth fifths rule")
        return False


def stat_demo_parity(df, trained=None, group=None):
    '''
        Calculates Statistical/Demo Parity on trained dataset
        :param df: trained data from user
        :return: None, prints if data successfully passed or failed the metric
    '''
    # predicted vs actual
    if trained is None:
        trained = input("Input predicted attribute\n")
    positiveValue = input("Input positive value(s): (ex: 'A, B, C, D')\n").split(", ")
    if group is None:
        group = input("Input group attribute\n")

    # initialises dictionary groupDict
    groupDict = dict()
    # print(trained, group, positiveValue)
    # print(df)
    # iterates through the trained column and group column of the dataframe
    for predicted_x, group_x in zip(df[trained], df[group]):
        # if the group name is not already in the dictionary, create a new dictionary definition and set the values
        # to [0,0] <- index 0 indicates number of positive rows for each specified group (group positive count),
        # index 1 indicates total number of rows for each specified group (group total count)
        if group_x not in groupDict:
            groupDict[group_x] = [0, 0]
        # if the trained value is what the user deems positive, it will increment both the group positive count and
        # the group total count, otherwise it will just increment the group total count
        if str(predicted_x) in positiveValue:
            groupDict[group_x] = [groupDict[group_x][0] + 1, groupDict[group_x][1] + 1]
        else:
            groupDict[group_x] = [groupDict[group_x][0], groupDict[group_x][1] + 1]
    # for each element of the dictionary: converts the group positive count and group total count into a decimal
    # percentage
    for x in groupDict:
        groupDict[x] = groupDict[x][0] / groupDict[x][1]
    # finds lowest percentage
    print(groupDict)
    lowestPositiveRate = min(groupDict.keys(), key=(lambda k: groupDict[k]))
    # finds highest percentage
    highestPositiveRate = max(groupDict.keys(), key=(lambda k: groupDict[k]))
    print(lowestPositiveRate, highestPositiveRate)

    result = fourFifths(groupDict[lowestPositiveRate], groupDict[highestPositiveRate])
    if result:
        print("Statistical/Demo Parity: Passed!")
    else:
        print("Statistical/Demo Parity: Failed!\n")
    return result


def disparate_impact(df, trained=None, group=None):
    '''
    Calculates Disparate impact metric on trained dataset
    :param df: trained data from user
    :return: None, prints if data successfully passed or failed the metric
    '''
    # get input from user to know trained attribute, group attribute, and positive value for trained attribute
    if trained is None:
        trained = input("Input trained attribute\n")
    positiveValue = input("Input positive value(s): (ex: 'A, B, C, D')\n").split(", ")
    if group is None:
        group = input("Input group attribute\n")
    # intializes dictionary groupDict
    groupDict = {}

    # iterates through the trained column and group column of the dataframe
    for trained_x, group_x in zip(df[trained], df[group]):
        # if the group name is not already in the dictionary, create a new dictionary definition and set the values
        # to [0,0] <- index 0 indicates number of positive rows for each specified group (group positive count),
        # index 1 indicates total number of rows for each specified group (group total count)
        if group_x not in groupDict:
            groupDict[group_x] = [0, 0]
        # if the trained value is what the user deems positive, it will increment both the group positive count and
        # the group total count, otherwise it will just increment the group total count
        if str(trained_x) in positiveValue:
            groupDict[group_x] = [groupDict[group_x][0] + 1, groupDict[group_x][1] + 1]
        else:
            groupDict[group_x] = [groupDict[group_x][0], groupDict[group_x][1] + 1]
    # for each element of the dictionary: converts the group positive count and group total count into a decimal
    # percentage
    for x in groupDict:
        groupDict[x] = groupDict[x][0] / groupDict[x][1]
        # print(x, ":", groupDict[x])
    # finds lowest percentage
    lowestPositiveRate = min(groupDict, key=groupDict.get)
    print("low:", groupDict[lowestPositiveRate])
    # finds highest percentage
    highestPositiveRate = max(groupDict, key=groupDict.get)
    print("high", groupDict[highestPositiveRate])
    # finds ratio but dividing the lowestpositiverate by the highestpositiverate
    ratio = groupDict[lowestPositiveRate] / groupDict[highestPositiveRate]
    print(groupDict)
    print(ratio)
    if ratio >= .8:
        print("Disparate Impact: Passed!")
    else:
        print("Disparate Impact: Failed!\n")
    return ratio


# UNUSED, IGNORE:
def getActualRates(df, actual_val, group):
    ''''
        determine actual rates
        :param df: dataframe
        :param actual_val: actual value
        :param group: group value
        :return: none
    '''
    allGroups = {}
    actualRates = {}
    total = 0
    for act_x, group_x in zip(df[actual_val], df[group]):
        if act_x not in actualRates:
            actualRates[act_x] = 1
        else:
            actualRates[act_x] += 1
        allGroups[group_x] = actualRates[act_x]
        total += 1
    for x in actualRates:
        actualRates[x] = actualRates[x] / total
    print(actualRates)
    return actualRates


def differences_in_squared_error(df, pred_val=None, actual_val=None, group=None):
    '''
    determeine differences in squared error
    :param df:
    :param pred_val:
    :param actual_val:
    :param group:
    :return:
    '''
    # get predicted value, actual value, and group attribute from user
    if pred_val is None:
        pred_val = input("Input predicted attribute\n")
    if actual_val is None:
        actual_val = input("Input actual attribute\n")
    if group is None:
        group = input("Input group attribute\n")

    # print("groupTotals:", groupTotals)
    getValForCalc = dict()
    # look at each row in the dataframe
    for pred_x, act_x, group_x in zip(df[pred_val], df[actual_val], df[group]):
        # add group_x as dict key
        # sum of all rows: (pred-act)^2
        if group_x not in getValForCalc:
            # initialize value of new key to (pred-act)^2 and count to be 1
            getValForCalc[group_x] = [pow(float(pred_x) - float(act_x), 2), 1]
            # print(getValForCalc[group_x])
        else:
            # cont summing (pred-act)^2 and incrementing count
            getValForCalc[group_x] = [getValForCalc[group_x][0] + pow(float(pred_x) - float(act_x), 2),
                                      getValForCalc[group_x][1] + 1]
    calcResult = []
    # calculate total result of sum/totalcount
    for x in getValForCalc:
        # print(x)
        calcResult.append(getValForCalc[x][0] / getValForCalc[x][1])

    # finds lowest percentage
    # print(calcResult)
    minVal = min(calcResult)
    # finds highest percentage
    maxVal = max(calcResult)

    print(minVal, maxVal)
    # apply the fourth fifths rule and print if it resulted in success or failure
    result = fourFifths(minVal, maxVal)
    if result:
        print("Differences In Squared Error: Passed!")
    else:
        print("Differences In Squared Error: Failed!")


def balance_btwn_subgroups(df, pred_val=None, actual_val=None, group=None):
    '''
    Calculates Balance for positive and negative class metric (score-based)
    :param df: trained data from user
    :return: None, prints if data successfully passed or failed the metric
    '''
    # get predicted value, actual value, and group attribute from user
    if pred_val is None:
        pred_val = input("Input predicted attribute\n")
    if actual_val is None:
        actual_val = input("Input actual attribute\n")
    if group is None:
        group = input("Input group attribute\n")
    # initializes dictionary groupDict
    groupDict = {}
    # initializes list of averages
    avgs = []
    # loop through the trained data looking at the predicted value, actual value, and group value
    for pred_x, act_x, group_x in zip(df[pred_val], df[actual_val], df[group]):
        # if the group is not in the dictionary, make a new key value pair - the key will be named after the group
        # the value is a list containing the absolute value of the difference between the predicted value
        # and actual value and an incrementation to find total number in that group
        if group_x not in groupDict:
            groupDict[group_x] = [abs(float(pred_x) - act_x), 1]
        else:
            groupDict[group_x][0] += abs(float(pred_x) - act_x)
            groupDict[group_x][1] += 1
        # print(pred_x, act_x)
    # print(groupDict)
    # loop through dictionary, dividing the difference by the total to get the probability
    for x in groupDict:
        # print(groupDict[x])
        avgs.append(abs(groupDict[x][0] / groupDict[x][1]))
    print(avgs)
    # finds lowest percentage
    minVal = min(avgs)
    # finds highest percentage
    maxVal = max(avgs)
    # apply the fourth fifths rule and print if it resulted in success or failure
    result = fourFifths(minVal, maxVal)
    if result:
        print("Balance for Positive and Negative Class: Passed!")
    else:
        print("Balance for Positive and Negative Class: Failed!")

def main():
    print("hello")

if __name__ == "__main__":
    main()
