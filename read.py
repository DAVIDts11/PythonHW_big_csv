import re
import numpy as np
import csv
import time

"""
Solution to the 2-nd H.W. task.
submited by :
    Tsibulsky David 309444065 and Nahoom Chen 316086479 
"""

def calcMaxVal(dataDictCdate, dictName):
    """
        This function is calculate the max occur value for each category in the month .
    :param dataDictCdate: dataDict[Cdate] - dictionary for the particular month
    :param dictName: str  - "hashTags"   or  "mentions"  or  "webs"
    :return: maxVal (ost occur value in category for the particular moth ) or "None"
    """
    if bool(dataDictCdate[dictName]):
        max = 0
        maxVal ="None"                # not nessery , only for warnings
        for k, v in dataDictCdate[dictName].items():
            if v > max:
                max = v
                maxVal = k
        return maxVal
    else:
        return "None"



def countOccurs(dictData,innerDick,itersRe):
    """
        This function gets from one tweet text all the values for the particular category ,
        and added the value to the corresponding date and set the counter of this value to one,
        if  this value already exist - it will only raise the counter for this value by one .
        (It treats  a little bit differently for some categories but there are manny line that same for all of them)
    :param dictData:  dataDict[tweet_date]  - dictionary for the particular month
    :param innerDick: str -  "hashTags" or "mentions" or "webs"
    :param itersRe: all the patterns that occur in this text for that category .  (iter for match objects)
    """
    for itr in itersRe:
        if innerDick == "webs":
            itr_string = itr.group(1)
        else:
            itr_string =itr.group()
        if innerDick == "hashTags":
            str_to_check = itr_string[1:].lower()                                   #.group(1)
            if str_to_check == "bitcoin" or str_to_check == "bitcoins" or str_to_check == "btc":
                continue
        if dictData[innerDick].get(itr_string) == None:
            dictData[innerDick].update({itr_string:1})
        else:
            dictData[innerDick][itr_string]+=1



def read_data_from_file():
    """
        This function is reading data from csv file "tweets.csv"  line by line with csv.DictReader ,
        and reurn dict with needed information and list of all months
    :return:
    1) dataDict = {month : {"hashTags":{hashtag1 : amount,hashtag1:amount, ... } , "mentions": { metion1: amount ,metion2: amount, ...} ,
                                                                    "webs": {web1: amount, web2:amount,.... }} }
    2)listDates = [yyyy-mm1 , yyyy-mm2 ,.....]
    """
    dataDict ={}
    listDates =[]
    hashPatern = "#([\w-]+)"
    mentPatern = "@[\w-]+"
    webPattern = "https*://([^/\s]*)"
    with open("./tweets/tweets.csv","r", encoding='utf8') as read_file:
        csv_dict = csv.DictReader(read_file,delimiter=';')
        for row in csv_dict:
            tweet_date = dict(row)["timestamp"][:7]     # (re.search("\d{4}-\d{2}", dict(row)["timestamp"])).group()          #####    [:7]
            tweet_hashTags = re.finditer(hashPatern, dict(row)["text"])
            tweet_mentions =re.finditer(mentPatern,dict(row)["text"])
            tweet_webs = re.finditer(webPattern,dict(row)["text"])
            if dataDict.get(tweet_date) == None:
                listDates.append(tweet_date)
                hashTagDict = {}
                mentionsDict = {}
                websDict = {}
                dataDict.update({tweet_date:{"hashTags": hashTagDict, "mentions": mentionsDict, "webs": websDict}})
            countOccurs(dataDict[tweet_date],"hashTags",tweet_hashTags)
            countOccurs(dataDict[tweet_date], "mentions", tweet_mentions)
            countOccurs(dataDict[tweet_date], "webs", tweet_webs)
    return dataDict,listDates







def write_data_to_file(dataDict,listDates):
    """
        This function is get dataDict and listDates that was produced by read_data_from_file function ,
        and write csv file (tweet-data.csv) that contains columns : Month,Hashtag,Mention,Website.
    :param dataDict: from the  read_data_from_file()
    :param listDates: from the read_data_from_file()
    """
    with open("./tweets/tweet-data.csv","w", encoding='utf8') as write_file:
        write_file.write("Month,Hashtag,Mention,Website\n")
        dateArray = np.array(listDates)
        dateArray.sort()
        for Cdate in dateArray :
            write_file.write(Cdate)
            write_file.write(",")
            write_file.write(calcMaxVal(dataDict[Cdate],"hashTags"))
            write_file.write(",")
            write_file.write(calcMaxVal(dataDict[Cdate], "mentions"))
            write_file.write(",")
            write_file.write(calcMaxVal(dataDict[Cdate], "webs"))
            write_file.write("\n")







if __name__ == "__main__":
    """
    main program that solve the task with measuring and printing the time that it takes to do that (in sec).  
    """
    start = time.time()
    dataDict, listDates = read_data_from_file()
    write_data_to_file(dataDict, listDates)
    end = time.time()
    print(end - start)




































# for hashTag in tweet_hashTags:
#     hashTagStr =hashTag.group()
#     str_to_check = hashTagStr[1:].lower()                                   #.group(1)
#     if str_to_check != "bitcoin" and str_to_check != "bitcoins" and str_to_check != "btc":
#         if dataDict[tweet_date]["hashTags"].get(hashTagStr) == None:
#             dataDict[tweet_date]["hashTags"].update({hashTagStr:1})
#         else:
#             dataDict[tweet_date]["hashTags"][hashTagStr]+=1
# for mention in tweet_mentions:
#     mentionStr = mention.group()
#     if dataDict[tweet_date]["mentions"].get(mentionStr) == None:
#         dataDict[tweet_date]["mentions"].update({mentionStr:1})
#     else:
#         dataDict[tweet_date]["mentions"][mentionStr]+=1
# for web in tweet_webs:
#     webStr = web.group(1)
#     if dataDict[tweet_date]["webs"].get(webStr) == None:
#         dataDict[tweet_date]["webs"].update({webStr:1})
#     else:
#         dataDict[tweet_date]["webs"][webStr]+=1
