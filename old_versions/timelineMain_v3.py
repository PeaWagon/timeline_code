#!/usr/bin/python3.5

# Python code to collect residue and file data from timeline tml file.
# JEN
# Tuesday 21st June, 2016
# Wednesday 6th July, 2016
# Monday 22nd August, 2016

# Version 3


############################################################################
#                               MAIN PROGRAM                               #
############################################################################

# NOTES FROM 22 AUGUST, 2016

# I added the functionality to the code to find the residue ranges
# and segment names from the file automatically (rather than having
# to input them every time as it's fucken annoying lol). DONE

# Want to add option to update .tml file with ProP file residue range
# (rather than 4-33 or 1-36 etc.) DONE

# Would like the functionality where the pwd is added automatically.
# Prevents annoying copy and pasting of really long directories

# NOTE: will have to fix the residue ranges and extend ProP_res list
# to include residues from extended ProP c-terminus. DONE

# Update 23 Aug, 2016 - need to make a new file that contains the updated
# ProP residue range because otherwise I won't be able to open the timeline
# file in VMD (dependencies won't match, I think). DONE

# Also I removed the turtle thing because it was annoying and useless :P

# Made the program print the information about the residue ranges first, so
# I can check to see if they are in need of updating before running the 
# analysis. Less opening of files woo. 

# Program now only asks to update the residue range if someone says it
# is a ProP c-terminus file. 

# Update: fixed the residue loops so now it doesn't ask you if you want
# to analyse another residue if you already said no to the first query.

from functionsTimeline_v3 import *

print("***************************************************************")
print("Welcome to Jen's Timeline Secondary Structure File Analysis.")
print("This is version 3, it should work.")
print("To quit at any time, type \"q\".")
print("***************************************************************")

while True:  
    
    #chespin = pikachu()
    #print(chespin)
    
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
    
    # Initialize test case into object class    
    test = Timeline(name, file_dir, filename, [], False)
    
    #  Get info from file
    sr = test.get_info_2()   
    
    # print sr info for error checking
    test.print_sr() 
    
    # Determine whether using ProP c-terminus (PCT)
    # If yes, ask whether person wants to update tml file.
    PCT = test.is_ProP()                # assign PCT
    while PCT == 3:                     # invalid input
        PCT = test.is_ProP()
    if PCT == 'q':
        break                           # quit 
                                        
    # Get file statistics?
    f_stat = test.get_file()
    while f_stat == 3:                  # invalid input
        f_stat = test.get_file()
    if f_stat == 'q':                   # quit
        break
    elif f_stat != 2:                   # yes file stats
        test.file_info()

    # Get residue statistics?
    r_stat = test.get_res()
    while r_stat == 3:                  # invalid input
        r_stat = test.get_res()
    if r_stat == 'q':                   # quit
        break
   
    print("***************************************************************")
    print("Type \"q\" to quit.")
    print("***************************************************************")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
