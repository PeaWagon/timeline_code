#!/usr/bin/python3.5

# Python code to collect residue and file data from timeline tml file.
# JEN
# Tuesday 21st June, 2016
# Wednesday 6th July, 2016
# Monday 22nd August, 2016
# Friday 6th January, 2017

# Version 4


############################################################################
#                               MAIN PROGRAM                               #
############################################################################

# NOTES FROM 6 JANUARY, 2017

# Now adding functionality to save file results to another file
# Idea here is to be able to autogenerate a csv file containing
# percent of time each simulation spends as a given secondary structure
# I can then make a R script that automatically plots the boxplots
# using this csv file
# An input will be a file name to save to
# You have the choice to create a new file or add to an existing one.

# current progress: prompts incorporated from user. They work nicely.
# Now need to add to class and implement opening csv for writing.
# Also need to figure out how I store the data so I can pull it
# out from the code easily. Hopefully previous me wasn't an ass hole.

# also going to try and add pwd to function to prevent having to
# add full path every time. DONE works like a charm!!!

# NOTES FROM JANUARY 18, 2017
# Small change. I added the three-letter codes to the residues
# so I know what they are (before only showed single-letter codes).
# Going to add ProP Ec and ProP Xc options... Done
# Going to change the residue input so that it only asks for a
# segment name if there is more than one option (aka don't want to 
# chose from a choice of 1...) Done

from functionsTimeline_v4 import *

print("***************************************************************")
print("Welcome to Jen's Timeline Secondary Structure File Analysis.")
print("This is version 4, it is in progress.")
print("To quit at any time, type \"q\".")
print("***************************************************************")

while True:  
    
    # TEST NAME 
    name = get_name()                   # assign name
    if name == "q":                     # quit
        break

    # TEST FILENAME    
    file_dir = get_dir()                # assign file_dir
    while file_dir == 1:                # invalid input
        file_dir = get_dir()
    if file_dir == "q":                 # quit
        break
    else:                               # assign filename
        last_slash = file_dir.rindex('/')
        filename = file_dir[last_slash+1:len(file_dir)]
    
    # Ask about saving data to csv file
    csv = get_csv()                     # assign CSV file
    while csv == 1:                     # invalid input
        csv = get_csv()
    if csv == "q":                      # quit
        break
    
    # Get csv name 
    csv_n = csv_name(csv, filename)     # csv = "Y" or False
    # False and code won't write a csv file    
    while csv_n == 1:
        csv_n = csv_name(csv, filename)
    
    # Initialize test case into object class    
    test = Timeline(name, file_dir, filename, [], False, csv_n)
    
    #  Get info from file
    sr = test.get_info_2()   
    
    # print sr info for error checking
    test.print_sr() 
    
    # Determine whether the file is from ProP
    # Determine whether ProP Ec or Xc is in the file
    # Give option to update ProP Ec file (if using 1-72 numbering).
    ProP = test.is_ProP()                # assign PCT
    while ProP == 3:                     # invalid input
        ProP = test.is_ProP()
    if ProP == 'q':
        break                           # quit 
                                        
    # Get file statistics?
    f_stat = test.get_file()
    while f_stat == 3:                  # invalid input
        f_stat = test.get_file()
    if f_stat == 'q':                   # quit
        break
    elif f_stat != 2:                   # yes file stats
        test.file_info()
#working here#
        test.write_csv()                # write csv data (where applicable)
        
    # Get residue statistics?
    r_stat = test.get_res()
    while r_stat == 3:                  # invalid input
        r_stat = test.get_res()
    if r_stat == 'q':                   # quit
        break
   
    print("***************************************************************")
    print("Type \"q\" to quit.")
    print("***************************************************************")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
