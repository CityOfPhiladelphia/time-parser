import pandas as pd

import os
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv()

INPUT_FILE = os.getenv('INPUT_FILE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')
# print(INPUT_FILE)

meals = pd.read_csv(INPUT_FILE)
print('type(meals):', type(meals))

days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# function to check whether value is NaN
def checkForNan(value):
    if pd.isna(value):
        return True
    else:
        return False

# function to check whether value includes any version of AM or PM
def checkForAMPM(value):
    allValues = ['AM', 'PM', 'am', 'pm', 'a.m.', 'p.m.', 'A.M.', 'P.M.']
    if checkForNan(value) == False:
        if any(x in value for x in allValues):
            return True
        else:
            return False
    else:
        return False

# function to check whether value includes any version of PM
def checkForPM(value):
    allValues = ['PM', 'pm', 'p.m.', 'P.M.']
    if checkForNan(value) == False:
        if any(x in value for x in allValues):
            return True
        else:
            return False
    else:
        return False

# function to check whether time value is 12
def checkIs12(value):
    if checkForNan(value) == False:
        if '12' in value:
            return True
        else:
            return False
    else:
        return False

# function to check whether time value is 10 or 11
def checkIs10or11(value):
    if checkForNan(value) == False:
        if '10' in value or '11' in value:
            return True
        else:
            return False
    else:
        return False

# function to check whether value includes a colon
def checkForColon(value):
    if checkForNan(value) == False:
        if ':' in value:
            return True
        else:
            return False
    else:
        return False

# function to check whether value includes any version of "LN" or "BK"
def checkForText(value):
    if checkForNan(value) == False:
        if 'LN' in value or 'Ln' in value or 'BK' in value or 'Bk' in value:
            return True
        else:
            return False
    else:
        return False

# function to return single time if the value includes a colon and AM or PM
def parseTimeWithColonAndAMPM(time):
    # print('parseTimeWithColonAndAMPM, time: ', time)
    hasPM = checkForPM(time.strip())
    timeBeforeColon = time.split(':')[0].strip()
    if (int(timeBeforeColon) < 10):
        timeBeforeColon = '0' + timeBeforeColon
    timeAfterColonWithAMPM = time.split(':')[1]
    timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    if (hasPM):
        if int(timeBeforeColon) == 12:
            return '12:' + timeAfterColon
        else:
            return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    else:
        return timeBeforeColon + ':' + timeAfterColon
    
# function to return single time if the value includes a colon and AM or PM
def parseStartTimeWithColonAndNoAMPMs(startTime, endTime):
    # print('parseTimeWithColonAndAMPM, time: ', time)
    # hasPM = checkForPM(time.strip())
    startTimeBeforeColon = startTime.split(':')[0].strip()
    if (int(startTimeBeforeColon) < 10):
        startTimeBeforeColon = '0' + startTimeBeforeColon
    startTimeAfterColon = startTime.split(':')[1]
    # timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    # if (hasPM):
    #     if int(timeBeforeColon) == 12:
    #         return '12:' + timeAfterColon
    #     else:
    #         return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    # else:
    return startTimeBeforeColon + ':' + startTimeAfterColon

# function to return single time if the value includes a colon and AM or PM
def parseEndTimeWithColonAndNoAMPMs(startTime, endTime):
    # print('parseTimeWithColonAndAMPM, time: ', time)
    # hasPM = checkForPM(time.strip())
    startTimeBeforeColon = startTime.split(':')[0].strip()
    endTimeBeforeColon = endTime.split(':')[0].strip()
    if (int(endTimeBeforeColon) < int(startTimeBeforeColon)):
        endTimeBeforeColon = str(int(endTimeBeforeColon) + 12)
    elif (int(endTimeBeforeColon) < 10):
        endTimeBeforeColon = '0' + endTimeBeforeColon
    endTimeAfterColon = endTime.split(':')[1]
    # timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    # if (hasPM):
    #     if int(timeBeforeColon) == 12:
    #         return '12:' + timeAfterColon
    #     else:
    #         return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    # else:
    return endTimeBeforeColon + ':' + endTimeAfterColon

# function to return single time if the value includes a colon, the start time does NOT include AM or PM, and the end time includes AM or PM
def parseTimeWithColonAndEndAMPM(time, endTime):
    # print('parseTimeWithColonAndEndAMPM, time: ', time)
    endHasPM = checkForPM(endTime.strip())
    endIs12 = checkIs12(endTime.strip())
    startIs10or11 = checkIs10or11(time.strip())
    timeBeforeColon = time.split(':')[0].strip()
    if (int(timeBeforeColon) < 10):
        timeBeforeColon = '0' + timeBeforeColon
    timeAfterColonWithAMPM = time.split(':')[1]
    timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    if (endHasPM):
        if int(timeBeforeColon) == 12:
            return '12:' + timeAfterColon
        elif endIs12 or startIs10or11:
            return timeBeforeColon + ':' + timeAfterColon
        else:
            return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    else:
        return timeBeforeColon + ':' + timeAfterColon

# function to return single time if the value does NOT include a colon and DOES include AM or PM
def parseTimeWithNoColonAndAMPM(time):
    hasPM = checkForPM(time)
    if (hasPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        if (int(re.split('a|A', time)[0].strip()) < 10):
            return '0' + re.split('a|A', time)[0].strip() + ':00'
        else:
            return re.split('a|A', time)[0].strip() + ':00'

# function to return single time if the value does NOT include a colon, the start time does NOT include AM or PM, and the end time includes AM or PM
def parseTimeWithNoColonAndEndAMPM(time, endTime):
    hasEndPM = checkForPM(endTime)
    endIs12 = checkIs12(endTime.strip())
    startIs10or11 = checkIs10or11(time.strip())
    if (hasEndPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        elif endIs12 or startIs10or11:
            return re.split('a|A', time)[0].strip() + ':00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        if (int(re.split('a|A', time)[0].strip()) < 10):
            return '0' + re.split('a|A', time)[0].strip() + ':00'
        else:
            return re.split('a|A', time)[0].strip() + ':00'

# function that takes a string that includes start and end time, and returns a list of the parsed start and end times
def parseMealWindowTimes(stringTime):
    # print('parseMealWindowTimes, stringTime:', stringTime)
    parsedTimes = pd.Series()
    isNan = checkForNan(stringTime)

    if (isNan or len(stringTime) == 0):
        parsedTimes[0] = ''
        parsedTimes[1] = ''
    else:
        startAndEndTimes = stringTime.split('-')
        startHasAMPM = checkForAMPM(startAndEndTimes[0])
        startHasColon = checkForColon(startAndEndTimes[0])
        endHasAMPM = checkForAMPM(startAndEndTimes[1])
        endHasColon = checkForColon(startAndEndTimes[1])
        startHasText = checkForText(startAndEndTimes[0])

        # remove BK and LN text from start and end times
        if (startHasText):
            startAndEndTimes[0] = startAndEndTimes[0].replace('BK', '').replace('Bk', '').replace('LN', '').replace('Ln', '').strip()
            startAndEndTimes[1] = startAndEndTimes[1].replace('BK', '').replace('Bk', '').replace('LN', '').replace('Ln', '').strip()
        
        # parse start time
        if (startHasAMPM and startHasColon):
            parsedTimes[0] = parseTimeWithColonAndAMPM(startAndEndTimes[0])
        elif (startHasAMPM and startHasColon == False):
            parsedTimes[0] = parseTimeWithNoColonAndAMPM(startAndEndTimes[0])
        elif (startHasAMPM == False and endHasAMPM and startHasColon):
            parsedTimes[0] = parseTimeWithColonAndEndAMPM(startAndEndTimes[0], startAndEndTimes[1])
        elif (startHasAMPM == False and endHasAMPM == False and startHasColon):
            parsedTimes[0] = parseStartTimeWithColonAndNoAMPMs(startAndEndTimes[0], startAndEndTimes[1])
        elif (startHasAMPM == False and endHasAMPM and startHasColon == False):
            parsedTimes[0] = parseTimeWithNoColonAndEndAMPM(startAndEndTimes[0], startAndEndTimes[1])
        elif (startHasAMPM == False and endHasAMPM == False and startHasColon == False):
            # print('startAndEndTimes[0]', startAndEndTimes[0], 'startAndEndTimes[1]', startAndEndTimes[1])
            parsedTimes[0] = startAndEndTimes[0] + ':00'
        else:
            parsedTimes[0] = startAndEndTimes[0]
        
        # parse end time
        if (endHasAMPM and endHasColon):
            parsedTimes[1] = parseTimeWithColonAndAMPM(startAndEndTimes[1])
        elif (endHasAMPM and endHasColon == False):
            parsedTimes[1] = parseTimeWithNoColonAndAMPM(startAndEndTimes[1])
        elif (endHasAMPM == False and endHasColon):
            parsedTimes[1] = parseEndTimeWithColonAndNoAMPMs(startAndEndTimes[0], startAndEndTimes[1])
        elif (endHasAMPM == False and endHasColon == False):
            # print('endHasAMPM == False and endHasColon == False startAndEndTimes:', startAndEndTimes)
            if (startAndEndTimes[1] > startAndEndTimes[0]):
                # print('startAndEndTimes[0]', startAndEndTimes[0], 'startAndEndTimes[1]', startAndEndTimes[1])
                parsedTimes[1] = str(int(startAndEndTimes[1])+12) + ':00'
            else:
                parsedTimes[1] = parseTimeWithNoColonAndAMPM(startAndEndTimes[1])
                # print('startAndEndTimes[0]', startAndEndTimes[0], 'startAndEndTimes[1]', startAndEndTimes[1], 'parsedTimes', parsedTimes)
        else:
            parsedTimes[1] = startAndEndTimes[1]

    return parsedTimes

# function that takes a string that potentially includes 2 meal windows, and returns a dataframe with the two meal windows split into two columns
def splitMealWindows(stringTimes):
    splitTimes1 = []
    splitTimes2 = []
    # splitTimes = stringTimes.str.split('&', n=1, expand=True)

    for stringTime in stringTimes:
        isNan = checkForNan(stringTime)
        if (isNan):
            splitTimes1.append('')
            splitTimes2.append('')
        else:
            splitTimes1.append(re.split('&|,|;|and', stringTime)[0].strip())
            if (len(re.split('&|,|;|and', stringTime)) > 1):
                splitTimes2.append(re.split('&|,|;|and', stringTime)[1].strip())
            else:
                splitTimes2.append('')
    
    splitTimesDf = pd.DataFrame({0: splitTimes1, 1: splitTimes2})
    return splitTimesDf

# loop through each day of the week
for day in days_list:
    print(day)
    # since some sites have two meals, use splitMealWindows to split the meals into two columns
    meals_both = splitMealWindows(meals[day])

    # parse the start and end times for the first (or only) meal
    meals_first_parsed = pd.Series()    
    for count, stringTime in enumerate(meals_both[0]):
        meals_first_parsed[count] = parseMealWindowTimes(stringTime)
        # print('meals_first_parsed[count]', meals_first_parsed[count], 'count:', count)
    meals_first_parsed_start = pd.Series()
    meals_first_parsed_end = pd.Series()
    for count, parsedTime in enumerate(meals_first_parsed):
        # print('parsedTime', parsedTime, 'parsedTime[0]', parsedTime[0], 'count:', count)
        meals_first_parsed_start[count] = parsedTime[0]
        meals_first_parsed_end[count] = parsedTime[1]

    # parse the start and end times for the second meal
    meals_second_parsed = pd.Series()    
    for count, stringTime in enumerate(meals_both[1]):
        meals_second_parsed[count] = parseMealWindowTimes(stringTime)
    meals_second_parsed_start = pd.Series()
    meals_second_parsed_end = pd.Series()
    for count, parsedTime in enumerate(meals_second_parsed):
        meals_second_parsed_start[count] = parsedTime[0]
        meals_second_parsed_end[count] = parsedTime[1]

    meals[day+'_start1']=meals_first_parsed_start
    meals[day+'_end1']=meals_first_parsed_end
    meals[day+'_start2']=meals_second_parsed_start
    meals[day+'_end2']=meals_second_parsed_end
    meals[day+'_exceptions']=''
    meals.drop(day, inplace=True, axis=1)

# TODO - handle days of the week with different capitalization

# list of datasets this COULD be used for:
# https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHL_COVID19_Testing_Sites_PUBLICVIEW/FeatureServer/0/query?where=1%3D1&outFields=*&f=pjson
# https://phl.carto.com/api/v2/sql?q=select+*+from+voting_sites+where+temporary_closure+%3D+%27FALSE%27+and+site_approved+%3D+%27TRUE%27

# print('meals', meals)
meals.to_csv(OUTPUT_FILE)