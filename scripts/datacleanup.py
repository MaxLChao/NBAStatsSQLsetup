import pandas as pd
import os
import re
import sys
os.chdir("/Users/Max_1/Documents/code/NBAStatsSQLsetup")
# take in directory
dir_in = sys.argv[1]
os.chdir(dir_in)

# we have a set of 9 different tables
# need to recognize each. 
# I think the easiest thing to do is probably just to cut the current headers
# add a new header that works and 
#load it in.
# function to add comma after player name
files = os.listdir()

# adds comma before the team name which is 3 capital letters
def commanames(lines):
    pattern=r'(\b)(?!III\b)([A-Z]{3})\b'
    replacement=r'\1, \2'
    mod_text = []
    for i in lines:
        mod = re.sub(pattern, replacement, i)
        mod_text.append(mod)
    return mod_text

#add commas after first comma
def commarest(lines):
    line_out = []
    for i in lines:
        parts = i.split(',',1)
        parts[1] = re.sub(r'(?<!^) ', ', ', parts[1])
        mod_line = ','.join(parts)
        line_out.append(mod_line)
    return line_out

#add a comma after index number
def indexcomma(lines):
    line_out = []
    for i in lines:
        mod_line = re.sub(r'^([^ ]+) ', r'\1, ', i)
        line_out.append(mod_line)
    return line_out

# clean up opponent
def commaswitch(lines):
    line_out = []
    pattern = r'(\d+\s+)([\w\'-]+(?:\sII|\sIII|\sIV|\sV|\sVI|\sJr\.|\sSr\.)?)\s*,\s*([\w\'-\.]+)(.*)'
    # super crazy regex to get the clean up
    # thank you ChatGPT
    def advancedmatch(match):
        return  f"{match.group(1)}{match.group(3)} {match.group(2)}, {match.group(4).strip()}"
    for i in lines:
        mod_line = re.sub(pattern, advancedmatch, i)
        line_out.append(mod_line)
    return line_out

# specific for estimated-advanced
def commanames_ea(lines):
    line_out =[]
    pattern = r"(\d+)\s+(.+?)\s+(.+?)\s+(\d+)\s+(\d+)\s+(\d+)"
    replacement = r"\1 \2 \3, \4 \5 \6"
    #def add_comma_after_name(match):
    #    return f"{match.group(1)}, {match.group(2).strip()}"
    for i in lines:
    	mod_line = re.sub(pattern, replacement, i)
    	line_out.append(mod_line)
    return line_out

def commarest_ea(text):
    #line_out =[]
    #for i in lines:
       #parts = i.split(',', 1)
       #first_part, second_part = parts
       #comma_added_second_part = re.sub(r'([^,\s]+)(?=\s|\Z)', r'\1,', second_part)
       #mod_line = first_part + ',' + comma_added_second_part
       #line_out.append(mod_line)
    #return line_out
    # Splitting the text at the first comma
    parts = text.split(',', 1)
    # If there's a second part, add commas after each space-separated element
    if len(parts) > 1:
        first_part, second_part = parts
        comma_added_second_part = re.sub(r'([^,\s]+)(?=\s|\Z)', r'\1,', second_part)
        return first_part + ',' + comma_added_second_part
    else:
        # If there's no initial comma, return the original text
        return text
    
for x in files: 
#advanced
#drop 1 row
    if x == "advanced.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/advanced_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[1:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/advanced.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/advanced.csv', 'a') as out:
            out.writelines(fin3)

#bio
# drop 1 row
# no index here
    elif x == "bio.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/bio_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[1:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/bio.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/bio.csv', 'a') as out:
            out.writelines(fin3)




#defense
#drop 10 rows
    elif x == "defense.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/defense_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[10:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/defense.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/defense.csv', 'a') as out:
            out.writelines(fin3)



#estimated-advanced
# drops 11 rows
# no team name here
    elif x == "estimated-advanced.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/estimated-advanced_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[11:]
        # add the comma after names
        fin = commanames_ea(lines)
        # commarest
        #fin2 = commarest_ea(fin)
        fin2 = [commarest_ea(text) for text in fin]
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/estimated-advanced.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/estimated-advanced.csv', 'a') as out:
            out.writelines(fin3)


# misc
# drop 12 rows
    elif x == "misc.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/misc_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[12:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/misc.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/misc.csv', 'a') as out:
            out.writelines(fin3)



# opponent
# 40 lines
# will need to reformat and remove the comma. then from here relabel the column first name/last name
    elif x == "opponent.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/opponent_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[40:]
        # fix the commas and switch
        fin = commaswitch(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/opponent.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/opponent.csv', 'a') as out:
            out.writelines(fin3)

#scoring
# 30 lines
    elif x == "scoring.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/scoring_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[30:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/scoring.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/scoring.csv', 'a') as out:
            out.writelines(fin3)


#traditional
# 1 line
    elif x == "traditional.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/traditional_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[1:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/traditional.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/traditional.csv', 'a') as out:
            out.writelines(fin3)


#usage
# 1 line
    elif x == "usage.txt":
        with open("/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/helpers/usage_header.txt",'r') as file:
            header = file.readlines()
        with open(x, 'r') as file:
            lines = file.readlines()[1:]
        # add the comma after names
        fin = commanames(lines)
        # commarest
        fin2 = commarest(fin)
        #comma index
        fin3 = indexcomma(fin2)
        # add in txt
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/usage.csv', 'w') as out:
            out.writelines(header)
        with open('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/usage.csv', 'a') as out:
            out.writelines(fin3)

# mkdir of match
dir_name = os.path.basename(os.path.normpath(dir_in))
path_out = '/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/' + dir_name
os.mkdir(path_out)
# mv all files into match
import shutil
for filename in os.listdir('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/'):
    if filename.endswith('.csv'):
        shutil.move(os.path.join('/Users/Max_1/Documents/code/NBAStatsSQLsetup/tables/cleaned/',filename), path_out)

