#!/usr/bin/python3.5

# Python code to collect residue and file data from timeline tml file.
# JEN
# Tuesday 21st June, 2016
# Wednesday 6th July, 2016

# Version 2


############################################################################
#                               MAIN PROGRAM                               #
############################################################################


# NOTES FROM 6 JULY, 2016

# Going to add the residue types (aka resid 1 == ARG, etc.)
# Going to implement turtle graphics for the amino acid residue.

# Sorta bug for turtle. Found a similar problem on internet:
# https://bugs.python.org/issue6639
# So essentially if I use turtle.done(), whereby the user must select
# the window's x to continue, and then try to use the turtle again
# within the same run of the program (i.e. for another residue)
# it doesn't work (something about threading that I don't quite get).

# The implications are that the turtle window stays open the whole time,
# and multiple residues can be written to the same window. 
# I have enabled a small hack where the turtle moves a slight bit down 
# depending on which residue number is being analyzed. This means that
# if two segment names share a residue number, calling both of them will
# result in the same residue being written in the same place (aka erase
# the old picta). This is not a problem but may need to be specified in 
# future documents if people are wondering why sometimes the residues 
# get drawn over.

# I have put the turtle_picta option behind a prompt. It works fine, but
# takes a stupid amount of time for my 12,500 frames to be drawn out.
# Turtle picta not recommended for large files.

# NOTES FROM 14 JULY, 2016

# I have added a part that prints the percent of time spent as a given
# secondary structure for the whole file.

# Now to try and add the list of residue IDs. DONE. Also added the 
# descriptor to the print statements. 

from functionsTimeline_v2 import *

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
    PCT = False
    test = Timeline(name, file_dir, filename, sr, PCT)
    
    # Determine whether using ProP c-terminus (PCT)
    PCT = test.is_ProP()                # assign PCT
    while PCT == 3:                     # invalid input
        PCT = test.is_ProP()
    if PCT == 'q':
        break                           # quit
        
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
