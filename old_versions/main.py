#!/usr/bin/python3.5

# Python code to collect residue and file data from timeline tml file.
# JEN
# Tuesday 21st June, 2016


############################################################################
#                               MAIN PROGRAM                               #
############################################################################


# NOTES FROM 21 JUNE:

# Need to add ability to choose segment IDs and amino acid ranges.
# Aka first segment = PROA
# amino acid range for PROA = 4-33 or 1-36 etc.
# DONE! :)

# NOTES FROM 22 JUNE:

# Need to enable filling in a path for the file. Aka so you don't need
# to be in the same directory as the file for it to be opened with this 
# code. Should do this last because it's not as important.

# Should probably add the filename to part of the class. Right now it gets
# referenced a whole lot and thus my code _could_ be more efficient.

# NOTES FROM 26 JUNE:

# Added filename and a few others to the class. The get name and get 
# directory functions are still outside of the class. This organization
# is needed to prevent errors initializing the class.

# I also added the feature that checks to see if the given directory
# actually contains the file that the person wants to check.

# Later on I need to improve the get_name function. This function
# is way too long and annoying. It should be looped.
# I also need a way to check if the format (i.e. does the range have
# a hyphen), and allow for the user to input again rather than
# closing the program abruptly.

# NOTES FROM 27 JUNE, 2016

# Made function get_res to reference is_valid function. If the user inputs
# a range that does not include the residue they want stats on, they will
# get an error.

# Need a warning if no matching full_id was found in the document.
# aka user input is consistent throughout program but their file
# does not contain any info on the segment they specified.

# Still need to improve get_name function. I think I will make sr
# a list and the length of said list will determine how many unique
# segments there are.

# NOTES FROM 28 JUNE, 2016

# Done the is_valid function.
# Done improving get_info function. It is now a part of the class.
# Note to self: can update a list in the object's list of self.thingies.

# There is no warning needed because the code now counts the number
# of lines matching a given residue ID (if the number is zero something
# really bad has happened or the person didn't put the right info
# into the get_info). 

# NOTES FROM 29 JUNE, 2016

# I have done the residue statistics. If I want, I can add a part to 
# tell you which frames correspond to the maximum secondary structure 
# phase (aka residue spent a maximum of 12 frames as a helix, and these
# frames are 1-12)

# The only way to improve this system right now would be to add a
# feature to pull the information from the file about the residue 
# ranges and segment IDs (that way you don't have to know them
# in order to analyse a file).

# Before I do more error checks, I'm going to add a loop so you can 
# analyse multiple residues before you are reprompted to enter a 
# simulation name.

from timeline import *

print("***************************************************************")
print("Welcome to Jen's Timeline Secondary Structure File Analysis.")
print("This code has moved out of the construction phase and is in the testing phase.")
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
    
    # Initialize test case into object class    
    sr = []
    test = Timeline(name, file_dir, filename, sr)
    
    # Get segment IDs:   
    sr = test.get_info()                # assign sr
    while sr == 3:                      # invalid input
        sr = test.get_info()
    if sr == 'q':                       # quit
        break
                                        
    # Get file statistics?
    f_stat = test.get_file()
    while f_stat == 3:                  # invalid input
        f_stat = test.get_file()
    if f_stat == 'q':                   # quit
        break
    elif f_stat != 2:                   # yes file stats
        test.file_info()

    # Get residue statistics?
    r_stat = test.get_res('first')
    while r_stat == 3:                  # invalid input
        r_stat = test.get_res('first')
    if r_stat == 'q':                   # quit
        break
    elif r_stat != 2:                   # yes residue stats
        full_id = r_stat                # format of resiude ID
        test.res_stats(full_id)         # gets info

    
    # Get another residue's statistics?
    more = test.next_res()
    while more != 'q':
        while more == 3:                # invalid input
            more = test.next_res()
        if more == 2:                   # no more residue stats
            break
        elif more == 1:                 # want more residue stats?
            more = test.next_res()
    else:
        break                           # quit
        
    print("***************************************************************")
    print("Type \"q\" to quit.")
    print("***************************************************************")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
