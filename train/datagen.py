import random
from datetime import date
import dateData

'''
Train data generator

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

def createDateTuples(dateStr: str, prep: str) -> tuple:
    '''
    Creates a tuple of (start, end, label) for a given dateStr
    '''
    start = len(prep)
    end = len(dateStr)
    return (start, end, "DATE")

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
    - DOTW, MM/DD
    - DOTW, YYYY/MM/DD

    Possible prepositions that may prepend exact dates:
    - on
    - for

    '''

    curYear = date.today().year
    preps = ["", "on ", "for "]

    exactDates = [] #list of dateStrs and their corresponding tuples of (start, end, label)
    
    for monthInt in range (1, 13):
        for dayInt in range (1, 32):
            for yearInt in range (curYear, curYear+3):
                if monthInt == 2 and dayInt > 28:
                    continue #skip this iteration and continue to next month
                monthStr = '0' + str(monthInt) if monthInt < 10 else str(monthInt)
                if monthStr in have30Days and dayInt > 30:
                    continue #skip this iteration and continue to next month
                #anything past this should be a month in have31Days
                dayStr = '0' + str(dayInt) if dayInt < 10 else str(dayInt)
                yearStr = str(yearInt)
                # MM/DD/YYYY, MM/DD, and YYYY/MM/DD forms ------------------------------------------------------------------------
                prep = random.choice(preps)
                dateStr = f"{prep}{monthStr}/{dayStr}/{yearStr}" # "on MM/DD/YYYY", "for MM/DD/YYYY" or "MM/DD/YYYY"
                exactDates.append((dateStr, createDateTuples(dateStr, prep)))

                prep = random.choice(preps)
                dateStr = f"{random.choice(preps)}{monthStr}/{dayStr}"# "on MM/DD", "for MM/DD" or "MM/DD
                exactDates.append((dateStr, createDateTuples(dateStr, prep)))

                prep = random.choice([preps[0], preps[2]])
                dateStr = f"{prep}{yearStr}/{monthStr}/{dayStr}" # "for YYYY/MM/DD" or "YYYY/MM/DD"
                exactDates.append((dateStr, createDateTuples(dateStr, prep)))

                # Month, DayInt, Year and Month, DayInt forms ---------------------------------------------------------------------
                monthStr = random.choice(dateData.months.get(monthInt)) #full month name or abbreviated
                monthStr = random.choice([monthStr.lower(), monthStr.lower().capitalize(), monthStr]) #lowercase, capitalized first letter, or all caps
                if len(monthStr) == 3: #if monthstr is abbreviated
                    monthStr = random.choice([monthStr, monthStr + '.']) #with or without period
                dayStr = dayIntsToStr(dayInt)
                prep = random.choice(preps)
                dateStr = f"{prep}{monthStr} {dayStr}, {yearStr}" # "on Month DayInt, Year" or "for Month DayInt, Year" or "Month DayInt, Year"
                exactDates.append((dateStr, createDateTuples(dateStr, prep)))

                prep = random.choice(preps)
                dateStr = f"{prep}{monthStr} {dayStr}" # "on Month DayInt" or "for Month DayInt" or "Month DayInt"
                exactDates.append((dateStr, createDateTuples(dateStr, prep)))
                
    return exactDates



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
    exactDates = genExactDates()
    writeTextToFile("train/exactDatePhrases.txt", exactDates)
main()