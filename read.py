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

    :param dataDictCdate:
    :param dictName:
    :return:
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

    :param dictData:
    :param innerDick:
    :param itersRe:
    :return:
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


# listDted =[]
# dataDict ={}

def read_data_from_file():
    """
        This function is reading data from csv file "tweets.csv"  line by line with csv.DictReader ,
        and
    :return:
    """
    dataDict ={}
    listDted =[]
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
                listDted.append(tweet_date)
                hashTagDict = {}  #{"maxOccueItem":None,"maxOccurAmount":0}
                mentionsDict = {}  #{"maxOccueItem":None,"maxOccurAmount":0}
                websDict = {}   #{"maxOccueItem":None,"maxOccurAmount":0}
                dataDict.update({tweet_date:{"hashTags": hashTagDict, "mentions": mentionsDict, "webs": websDict}})
            countOccurs(dataDict[tweet_date],"hashTags",tweet_hashTags)
            countOccurs(dataDict[tweet_date], "mentions", tweet_mentions)
            countOccurs(dataDict[tweet_date], "webs", tweet_webs)
    return dataDict,listDted







def write_data_to_file(dataDict,listDted):
    """

    :param dataDict:
    :param listDted:
    :return:
    """
    with open("./tweets/tweet-data.csv","w", encoding='utf8') as write_file:
        write_file.write("Month,Hashtag,Mention,Website\n")
        dateArray = np.array(listDted)
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
    
    """
    start = time.time()
    dataDict, listDted = read_data_from_file()
    write_data_to_file(dataDict, listDted)
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
