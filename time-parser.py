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

# function to check whether value includes a colon
def checkForColon(value):
    if checkForNan(value) == False:
        if ':' in value:
            return True
        else:
            return False
    else:
        return False

# function to return single time if the value includes a colon and AM or PM
def hasColonAndAMPM(time):
    print('hasColonAndAMPM, time: ', time)
    hasPM = checkForPM(time.strip())
    timeBeforeColon = time.split(':')[0].strip()
    timeAfterColonWithAMPM = time.split(':')[1]
    timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    if (hasPM):
        if int(timeBeforeColon) == 12:
            return '12:' + timeAfterColon
        else:
            return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    else:
        return timeBeforeColon + ':' + timeAfterColon

# function to return single time if the value includes a colon, the start time does NOT include AM or PM, and the end time includes AM or PM
def hasColonAndEndAMPM(time, endTime):
    print('hasColonAndEndAMPM, time: ', time)
    hasPM = checkForPM(endTime.strip())
    timeBeforeColon = time.split(':')[0].strip()
    timeAfterColonWithAMPM = time.split(':')[1]
    timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    if (hasPM):
        if int(timeBeforeColon) == 12:
            return '12:' + timeAfterColon
        else:
            return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    else:
        return timeBeforeColon + ':' + timeAfterColon

# function to return single time if the value does NOT include a colon and DOES include AM or PM
def hasNoColonAndAMPM(time):
    hasPM = checkForPM(time)
    if (hasPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        return re.split('a|A', time)[0].strip() + ':00'

# function to return single time if the value does NOT include a colon, the start time does NOT include AM or PM, and the end time includes AM or PM
def hasNoColonAndEndAMPM(time, endTime):
    hasEndPM = checkForPM(endTime)
    if (hasEndPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        return re.split('a|A', time)[0].strip() + ':00'

# function that takes a string that includes start and end time, and returns a list of the parsed start and end times
def parseMealTimes(stringTime):
    parsedTimes = pd.Series()
    isNan = checkForNan(stringTime)

    if (isNan):
        parsedTimes[0] = ''
        parsedTimes[1] = ''
    else:
        startAndEndTimes = stringTime.split('-')
        startHasAMPM = checkForAMPM(startAndEndTimes[0])
        startHasColon = checkForColon(startAndEndTimes[0])
        endHasAMPM = checkForAMPM(startAndEndTimes[1])
        endHasColon = checkForColon(startAndEndTimes[1])

        if (startHasAMPM and startHasColon):
            parsedTimes[0] = hasColonAndAMPM(startAndEndTimes[0])
        elif (startHasAMPM and startHasColon == False):
            parsedTimes[0] = hasNoColonAndAMPM(startAndEndTimes[0])
        elif (startHasAMPM == False and endHasAMPM and startHasColon):
            parsedTimes[0] = hasColonAndEndAMPM(startAndEndTimes[0], startAndEndTimes[1])
        elif (startHasAMPM == False and endHasAMPM and startHasColon == False):
            parsedTimes[0] = hasNoColonAndEndAMPM(startAndEndTimes[0], startAndEndTimes[1])
        else:
            parsedTimes[0] = startAndEndTimes[0]
        
        if (endHasAMPM and endHasColon):
            parsedTimes[1] = hasColonAndAMPM(startAndEndTimes[1])
        elif (endHasAMPM and endHasColon == False):
            parsedTimes[1] = hasNoColonAndAMPM(startAndEndTimes[1])
        else:
            parsedTimes[1] = startAndEndTimes[1]

    return parsedTimes

# loop through each day of the week
for day in days_list:
    # since some sites have two meals, split the meals into two columns
    meals_both = meals[day].str.split('&', n=1, expand=True)

    # parse the start and end times for the first (or only) meal
    meals_first_parsed = pd.Series()    
    for count, stringTime in enumerate(meals_both[0]):
        meals_first_parsed[count] = parseMealTimes(stringTime)
    meals_first_parsed_start = pd.Series()
    meals_first_parsed_end = pd.Series()
    for count, parsedTime in enumerate(meals_first_parsed):
        meals_first_parsed_start[count] = parsedTime[0]
        meals_first_parsed_end[count] = parsedTime[1]

    # parse the start and end times for the second meal
    meals_second_parsed = pd.Series()    
    for count, stringTime in enumerate(meals_both[1]):
        meals_second_parsed[count] = parseMealTimes(stringTime)
    meals_second_parsed_start = pd.Series()
    meals_second_parsed_end = pd.Series()
    for count, parsedTime in enumerate(meals_second_parsed):
        meals_second_parsed_start[count] = parsedTime[0]
        meals_second_parsed_end[count] = parsedTime[1]

    meals[day+'_start1']=meals_first_parsed_start
    meals[day+'_end1']=meals_first_parsed_end
    meals[day+'_start2']=meals_second_parsed_start
    meals[day+'_end2']=meals_second_parsed_end

meals.to_csv(OUTPUT_FILE)