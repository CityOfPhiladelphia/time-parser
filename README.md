# time-parser

time-parser is a script which reads in a csv, parses strings that hold time information, and breaks them into fields that hold standardized 24-hour time strings.  It outputs a second csv.

![](https://readme-github-images.s3.amazonaws.com/time-parser/csv_after_parse_01.PNG)

You can put the file paths into an .env file within the project:

    INPUT_FILE=C:\Users\YOUR_NAME\Projects\time-parser\inputOutput\COVID19_FreeMealSites_0.csv
    OUTPUT_FILE=C:\Users\YOUR_NAME\Projects\time-parser\inputOutput\COVID19_FreeMealSites_1.csv

### The string stuctures that are handled include:

7:30AM - 12PM (1 time has a colon, both times have AM or PM)

12:00-1:30PM (both times have colons, only the 2nd time has an AM or PM)

11AM - 1PM (neither time has a colon, both times have AM or PM)

2-3pm (neither time has a colon, only the 2nd time has an AM or PM)

10-11am & 4:30-6 PM (2 times windows with different combinations of the structures above)


### General rules:

Uppercase and lowercase "AM" and "pm", and including periods between the letters (a.m.) are all handled.

Spaces or lack of spaces between the times and the dashes are all handled.

### 4 main parsing functions:

function: parseTimeWithColonAndAMPM

    7:30AM - 12PM --> | 7:30 | 12:00 |

function: parseTimeWithColonAndEndAMPM

    12:00-1:30PM --> | 12:00 | 13:30 |

function: parseTimeWithNoColonAndAMPM

    11AM - 1PM --> | 11:00 | 13:00 |

function: parseTimeWithNoColonAndEndAMPM

    2-3pm --> | 14:00 | 15:00 |

### handling 2 time windows:

    10-11am & 4:30-6 PM --> | 10:00 | 11:00 | 16:30 | 18:00 |

### handling special cases:

When the first time within a window does not have and AM or PM, but the 2nd time DOES have an AM or PM, it uses the AM or PM of the 2nd time to parse the first time.  This could potentially cause confusion for time windows around the noon time of day.  If you use the PM for both in "11:00 - 12:00 PM", the 11:00 will get changed to 23:00.

    BK 8-8:30 AM, LN 11-12PM --> | 8:00 | 8:30 | 23:00 | 12:00 | 

Special checks have been put in, to keep "11:00AM" as "11:00" in those scenarios:

    BK 8-8:30 AM, LN 11-12PM --> | 8:00 | 8:30 | 11:00 | 12:00 | 
