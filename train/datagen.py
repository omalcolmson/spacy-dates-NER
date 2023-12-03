import random
from datetime import date
import dateData

'''
Train data generator

The goal of this document is to generate data for training/refining spaCy's NER model for better date and time recognition 

Train Data format:
TRAIN_DATA = [
    (str, {
        'entities': [(start, end, label), (start, end, label),...]
    }), 
    ...
'''

have31Days = [
        "january",
        "march",
        "may",
        "july",
        "august",
        "october",
        "december",
        "01",
        "03",
        "05",
        "07",
        "08",
        "10",
        "12",
        "jan",
        "mar",
        "may",
        "jul",
        "aug",
        "oct",
        "dec",
    ]

have30Days = [
    "april",
    "june",
    "september",
    "november",
    "04",
    "06",
    "09",
    "11",
    "apr",
    "jun",
    "sept",
    "nov",
]

def dayIntsToStr(dayInt: int) -> str:
    '''
    For handling converting the day as an integer to a string with the appropriate suffixes of "st", "nd", "rd", or "th"
    
    '''

    if dayInt > 3 and dayInt < 21:
            dayStr = str(dayInt) + "th"
    else:
        remainder = dayInt % 10
        if remainder == 1:
            dayStr = str(dayInt) + "st"
        elif remainder == 2:
            dayStr = str(dayInt) + "nd"
        elif remainder == 3:
            dayStr = str(dayInt) + "rd"
        else:
            dayStr = str(dayInt) + "th"

    return dayStr

def createDateTuples(dateStr: str, prep: str, label: str) -> tuple:
    '''
    Creates a tuple of (start, end, label) for a given dateStr
    '''
    start = len(prep)
    end = len(dateStr)
    return (start, end, label)

def handleDateStrVars(dateStr: str) -> str:
    dateStr = random.choice([dateStr, dateStr.lower(), dateStr.lower().capitalize()])
    if len(dateStr) == 3:
        datrStr = random.choice([dateStr, dateStr + '.', dateStr + ','])
    return dateStr

def genExactDates() -> list:
    '''
    Exact Date Formats: (DOTW = Day of the Week)
    - MM/DD/YYYY
    - MM/DD (current year implied)
    - YYYY/MM/DD
    - Month, DayInt, Year
    - Month, DayInt (current year implied)
    - DOTW, Month, DayInt, Year (e.g., Monday, January 1st, 2020)
    - DOTW, Month, DayInt (current year implied)
    - DOTW, MM/DD/YYYY
    - DOTW, MM/DD (current year implied)
    - DOTW, YYYY/MM/DD

    Possible prepositions that may prepend exact dates:
    - on
    - for

    '''

    curYear = date.today().year
    preps = ["", "on ", "for "]
    label = "DATE"

    exactDates = [] #list of dateStrs and their corresponding tuples of (start, end, label)
    
    for monthInt in range (1, 13):
        for dayInt in range (1, 32):
            for yearInt in range (curYear, curYear+3):
                if monthInt == 2 and dayInt > 28:
                    continue #skip this iteration and continue to next month
                monthStr = random.choice(['0' + str(monthInt), str(monthInt)]) if monthInt < 10 else str(monthInt)
                if ('0' + str(monthInt) if monthInt < 10 else str(monthInt)) in have30Days and dayInt > 30:
                    continue #skip this iteration and continue to next month
                #anything past this should be a month in have31Days
                dayStr = random.choice(['0' + str(dayInt), str(dayInt)]) if dayInt < 10 else str(dayInt)
                yearStr = str(yearInt)
                # MM/DD/YYYY, MM/DD, and YYYY/MM/DD forms ------------------------------------------------------------------------
                prep = random.choice(preps)
                dateStr = f"{prep}{monthStr}/{dayStr}/{yearStr}" # "on MM/DD/YYYY", "for MM/DD/YYYY" or "MM/DD/YYYY"
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                prep = random.choice(preps)
                dateStr = f"{random.choice(preps)}{monthStr}/{dayStr}"# "on MM/DD", "for MM/DD" or "MM/DD
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                prep = random.choice([preps[0], preps[2]])
                dateStr = f"{prep}{yearStr}/{monthStr}/{dayStr}" # "for YYYY/MM/DD" or "YYYY/MM/DD"
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                # Month, DayInt, Year and Month, DayInt forms ---------------------------------------------------------------------
                monthStr = random.choice(dateData.months.get(monthInt)) #full month name or abbreviated
                monthStr = handleDateStrVars(monthStr) #handles all format variations of lowercase, uppercase, capitalized, and abbrev w or w/o period
                dayStr = dayIntsToStr(dayInt)
                prep = random.choice(preps)
                dateStr = f"{prep}{monthStr} {dayStr}, {yearStr}" # "on Month DayInt, Year" or "for Month DayInt, Year" or "Month DayInt, Year"
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                monthStr = random.choice(dateData.months.get(monthInt)) #full month name or abbreviated
                monthStr = handleDateStrVars(monthStr) #handles all format variations of lowercase, uppercase, capitalized, and abbrev w or w/o period
                prep = random.choice(preps)
                dateStr = f"{prep}{monthStr} {dayStr}" # "on Month DayInt" or "for Month DayInt" or "Month DayInt"
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))
                
                # other forms that include specifying the day of the week ----------------------------------------------------------
                theDate = date(yearInt, monthInt, dayInt)
                dotwAsStr = random.choice(dateData.daysOfTheWeek[theDate.isoweekday()])
                dotwAsStr = handleDateStrVars(dotwAsStr)
                monthStr = random.choice(dateData.months.get(monthInt)) #full month name or abbreviated
                monthStr = handleDateStrVars(monthStr) #handles all format variations of lowercase, uppercase, capitalized, and abbrev w or w/o period
                prep = random.choice(preps)
                dateStr = f"{prep}{dotwAsStr}, {monthStr} {dayStr}, {yearStr}" # "on DOTW, Month DayInt, Year" or "for DOTW, Month DayInt, Year" or "DOTW, Month DayInt, Year"
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                dotwAsStr = random.choice(dateData.daysOfTheWeek[theDate.isoweekday()])
                dotwAsStr = handleDateStrVars(dotwAsStr)
                monthStr = '0' + str(monthInt) if monthInt < 10 else str(monthInt)
                dayStr = '0' + str(dayInt) if dayInt < 10 else str(dayInt)
                prep = random.choice(preps)
                dateStr = f"{prep}{dotwAsStr}, {monthStr}/{dayStr}/{yearInt}" # "on DOTW, MM/DD/YYYY" or "for DOTW, MM/DD/YYYY" or "DOTW, MM/DD/YYYY" 
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))
                dateStr = f"{prep}{dotwAsStr}, {yearInt}/{monthStr}/{dayStr}" # "on DOTW, YYYY/MM/DD" or "for DOTW, YYYY/MM/DD" or "DOTW, YYYY/MM/DD"  
                exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                if yearInt == curYear:
                    dotwAsStr = random.choice(dateData.daysOfTheWeek[theDate.isoweekday()])
                    dotwAsStr = handleDateStrVars(dotwAsStr)
                    monthStr = random.choice(dateData.months.get(monthInt)) #full month name or abbreviated
                    monthStr = handleDateStrVars(monthStr) #handles all format variations of lowercase, uppercase, capitalized, and abbrev w or w/o period
                    prep = random.choice(preps)
                    dateStr = f"{prep}{dotwAsStr}, {monthStr} {dayStr}" # "on DOTW, Month DayInt" or "for DOTW, Month DayInt" or "DOTW, Month DayInt" all for the current year
                    exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

                    dotwAsStr = random.choice(dateData.daysOfTheWeek[theDate.isoweekday()])
                    dotwAsStr = handleDateStrVars(dotwAsStr)
                    monthStr = random.choice(['0' + str(monthInt), str(monthInt)]) if monthInt < 10 else str(monthInt)
                    dayStr = random.choice(['0' + str(dayInt), str(dayInt)]) if dayInt < 10 else str(dayInt)
                    prep = random.choice(preps)
                    dateStr = f"{prep}{dotwAsStr}, {monthStr}/{dayStr}" # "on DOTW, MM/DD" or "for DOTW, MM/DD" or "DOTW, MM/DD" all for the current year
                    exactDates.append((dateStr, createDateTuples(dateStr, prep, label)))

    return exactDates

def genExactTimes() -> list:
    '''
    Exact Time Formats: 
    
    - HH:MM (24hr)
    - HH:MM (12hr)

    Possible prepositions that may prepend exact times:
    - at
    - for

    Possible time of day phrases that may follow exact times:
    - in the morning
    - in the afternoon
    - in the evening
    - at night
    - am, AM, a.m., A.M.
    - pm, PM, p.m., P.M.
    - o'clock
    - hours (for 24 hour time)

    '''
    exactTimes = [] #list of timeStrs and their corresponding tuples of (start, end, label)
    preps = ["", "at ", "for "]
    amLabel = "AM TIME"
    pmLabel = "PM TIME"
    amTimePhrases = [" am", " AM", " a.m.", " A.M.", " in the morning", ""]
    pmTimePhrases = [" pm", " PM", " p.m.", " P.M.", " in the afternoon", " in the evening", " at night", ""]
    prepTimePhrases = [" in the morning", " in the afternoon", " in the evening", " at night", ""] #can be used with or without "o'clock"
    oClock = [" o'clock", ""]
    #TODO
    for minute in range(0, 60):
        for hour in range(1, 13): #morning times
            hourStr = random.choice(['0' + str(hour), str(hour)]) if hour < 10 else str(hour)
            minuteStr = '0' + str(minute) if minute < 10 else str(minute)

            #morning times
            prep = random.choice(preps)
            amTimePhrase = random.choice(amTimePhrases)
            if amTimePhrase == " in the morning":
                timeStr = f"{prep}{hourStr}:{minuteStr}{oClock[0]}{amTimePhrase}" # "at HH:MM o'clock in the morning" or "for HH:MM o'clock in the morning"
            else:
                timeStr = f"{prep}{hourStr}:{minuteStr}{oClock[1]}{amTimePhrase}" # "at HH:MM am" or "for HH:MM am" or "HH:MM am"
            exactTimes.append((timeStr, createDateTuples(timeStr, prep, amLabel)))
        
        for hour in range(12, 0, -1): #afternoon times, going backwards from 12 to 1 pm
            hourStr = random.choice(['0' + str(hour), str(hour)]) if hour < 10 else str(hour)
            minuteStr = '0' + str(minute) if minute < 10 else str(minute)

            #afternoon times
            prep = random.choice(preps)
            pmTimePhrase = random.choice(pmTimePhrases)
            if pmTimePhrase.count("p") == 0: #if time phrase doesn't include pm in any form
                timeStr = f"{prep}{hourStr}:{minuteStr}{oClock[0]}{pmTimePhrase}" #can include o'clock
            else:
                timeStr = f"{prep}{hourStr}:{minuteStr}{oClock[1]}{pmTimePhrase}" #don't include o'clock
            exactTimes.append((timeStr, createDateTuples(timeStr, prep, pmLabel)))
        
        for hour in range(0, 24): #for 24 hour time, which should start at 0:00 and end at 23:59
            hourStr = random.choice(['0' + str(hour), str(hour)]) if hour < 10 else str(hour)
            minuteStr = '0' + str(minute) if minute < 10 else str(minute)
            label = amLabel if hour < 12 else pmLabel
            #24 hour time
            prep = random.choice(preps)
            timeStr = f"{prep}{hourStr}:{minuteStr} hours"
            exactTimes.append((timeStr, createDateTuples(timeStr, prep, label)))
            
            prep = random.choice(preps)
            timeStr = f"{prep}{hourStr}:{minuteStr}"
            exactTimes.append((timeStr, createDateTuples(timeStr, prep, label)))

            prep = random.choice(preps)
            timeStr = f"{prep}{hourStr}{minuteStr} hours"
            exactTimes.append((timeStr, createDateTuples(timeStr, prep, label)))

    return exactTimes

def writeTextToFile( fileName: str, textList: list) -> None:
    '''
    Writes the given text to the given file name
    '''
    with open(fileName, "w") as f:
        for text in textList:
            f.write(text[0] + "\n")


def main():
    # with open("train/timePhrases.txt", "w") as f:
    #     f.write(f"{dateData.daysOfTheWeekAsStrs}\n")
    #     f.write("\n")
    # aDate = exactDates[0] #should extract the tuple (dateStr, (start, end, label))
    # start = aDate[1][0]
    # end = aDate[1][1]
    # print(aDate[0], aDate[0][start:end])
    
    exactDates = genExactDates()
    writeTextToFile("train/exactDatePhrases.txt", exactDates)
    exactTimes = genExactTimes()    
    writeTextToFile("train/exactTimePhrases.txt", exactTimes)
main()