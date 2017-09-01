# Python code to analyze .tml data files from the timeline plugin
# from VMD.

# JEN

# Monday 20th June, 2016

# NOTE: structure of tml file (per line):
    # residue number  
    # "P" (no idea what this is) 
    # PROA or PROB
    # frame number
    # letter code denoting secondary structure
    # T=turn, H=alpha helix, E=extended config. 
    # B=isolated bridge, G=3-10 helix, I=pi-helix
    # C=coil (none of the above)
    
# NOTE: the above info starts on the tenth line. 

import os
import statistics

class Timeline(object):
    
    names = ['turn(s)', 'alpha heli(x/ces)', 'extended configuration(s)', 'isolated bridge(s)', 'pi heli(x/ces)', '3-10 heli(x/ces)', 'coil(s)']
    names2 = ['turn.', 'alpha helix.', 'extended configuration.', 'isolated bridge.', 'pi helix.', '3-10 helix.', 'coil.']
    names3 = ['turn', 'alpha helix', 'extended configuration', 'isolated bridge', 'pi helix', '3-10 helix', 'coil']
    letters = ['T','H','E','B','I','G','C']
    
    def __init__(self, name, file_dir, filename, sr):
        self.name = name
        self.file_dir = file_dir
        self.filename = filename
        self.sr = sr
    
    # Get information on residue IDs and segment names
    
    def get_info(self):
        print()
        print("***************************************************************")
        segments = input("How many segments (with unique amino acid ranges) are in " + self.filename+"? For instance, PROA 1-3 and PROA 23-25 count as two unique segments. ")
        if segments == 'q':
            return 'q'
        else:
            try:
                segments = int(segments)
            except ValueError:
                print("You should have input a number. Try again or type \"q\" to quit.")
                return 3
        print("Make sure the format (e.g. capitalization) for your segments is the same as what is in your file. Example: PROA.")
        print("Make sure that the given amino acid ranges are separated by a hyphen. Do not put spaces. It is assumed that each amino acid increases the range by 1. The range can start from any positive integer or zero. Examples 1-5, 0-20, 5-34.")
        print("***************************************************************")
        print()
        for i in range(segments):
            segment1 = input("Enter segment number "+str(i+1)+": ")
            if segment1 == "q":
                return 'q'
            else:
                AA1 = input("Enter the amino acid range for segment number "+str(i+1)+", separated by a hyphen: ")
                if AA1 == 'q':
                    return 'q'
                elif AA1.count('-') == 0:
                    print("Missing hyphen. Try again or type \"q\" to quit.")
                    return 3
                else:
                    hyphen = AA1.index('-')
                    first = int(AA1[0:hyphen])
                    last = int(AA1[hyphen+1:len(AA1)])
                    AA1 = list(range(first, last+1))
                    self.sr.append(segment1)
                    self.sr.append(AA1)
        return self.sr     
    
    # Allow user to get file statistics

    def get_file(self):
        gen_stat = input("Return file statistics? (Y/n) ")
        if gen_stat == "Y":
            print("General file statistics will now be reported for " + self.name + '.')
            return 1
        elif gen_stat == "n":
            print("General file statistics will be skipped.")
            return 2 
        elif gen_stat == "q":
            return 'q'
        else:
            print("Invalid input. Try again, or press \"q\" to quit.")
            return 3
    
    # Allow user to choose specific segment/residue IDs

    def get_res(self, first_or_restart):
        if first_or_restart == 'restart':
            res_stat = 'Y'
        elif first_or_restart == 'first':
            res_stat = input("Return specific residue statistics? (Y/n) ")
        
        # User wants residue statistics
        if res_stat == "Y":
            print()
            print("The available residue IDs are:")
            for i in range(0,len(self.sr),2):
                print("Segment ID "+ str(int(i/2)+1) + ": " + self.sr[i])
                print("Residue Range "+ str(int(i/2)+1) + ": "  + str(self.sr[i+1]))
            print()
            seg = input("Specify the segment you are interested in (example PROA). Make sure the format (e.g. capitalization) is the same as what is in your file: ")
            if seg == 'q':
                return 'q'
            else:
                res = input("Specify the residue number you are interested in (example 4): ")
                if res == 'q':
                    return 'q'
                else:
                    try:
                        res = int(res)
                    except ValueError:
                        print("You should have input a number. Try again, or type \"q\" to quit.")
                        return 3
                # Checks to make sure residue is valid.
                full_id = str(res)+' '+self.get_letter()+' '+str(seg)
                if self.is_valid(full_id) == True:
                    print("Residue statistics will now be reported for segment " + seg + ", residue number " + str(res) + '.')
                    return full_id
                else:
                    print("Residue segment and number do not match the segments and ranges that were given. Try again, or type \"q\" to quit.")
                    return 3
        
        # User does not want residue statistics
        elif res_stat == "n":
            print("Residue file statistics will be skipped.")
            return 2
        elif res_stat == "q":
            return 'q'
        else:
            print("Invalid input. Try again, or type \"q\" to quit.")
            return 3
    
    # Determines what should be searched for in the file.
    # Checks to make sure that the searched string is in the same format as
    # what was inputted during get_info() function (aka get segment IDs).

    def is_valid(self, full_id):
        print()
        print("Checking that the given residue ID is valid.")
        sr_c = self.sr[:]
        last_space = full_id.rindex(' ')
        segment = full_id[last_space+1:len(full_id)]
        num = int(full_id[0:full_id.index(' ')])
        # Checks multiple of the same segment ID if applicable.
        # I.e. I included PROA 1-5 and PROA 9-10 as input.
        while sr_c.count(segment) > 0:
            sind = sr_c.index(segment)
            rind = sind + 1
            if sr_c[rind].count(num) == 1:
                print("Residue "+segment+' '+str(num)+" is in the given range(s).")
                print()
                return True
            else:
                sr_c.remove(segment)
        else:
            return False    
    
    # Gets info for another residue if requested.
    
    def next_res(self):
        query = input("Would you like to analyse another residue? (Y/n) ")
        if query == 'q':
            return 'q'
        elif query == 'Y':
            r_stat = self.get_res('restart')
            while r_stat == 3:                  # invalid input
                r_stat = self.get_res('restart')
            if r_stat == 'q':                   # quit
                return 'q'
            elif r_stat != 2:                   # yes residue stats
                full_id = r_stat                # format of resiude ID
                self.res_stats(full_id)         # gets info
                return 1            
        elif query == 'n':
            return 2
        else:
            print("Invalid input. Try again, or type \"q\" to quit.")
            return 3
    
    
    def get_letter(self):
        """ Finds the identity of the random letter/string
            in the tml file after the residue number.
        """
        with open(self.file_dir, 'r') as f:
            for line in f:
                if line[0] != "#":
                    space1 = line.index(' ')
                    line2 = line[0:space1]+line[space1+1:len(line)]
                    space2 = line2.index(' ')
                    letter = line[space1+1:space2+1]
                    return letter
                        
    # letter code denoting secondary structure
    # T=turn, H=alpha helix, E=extended config. 
    # B=isolated bridge, I=pi-helix, G=3-10 helix 
    # C=coil (none of the above)               
    
    def get_sstruct(self, search_string):
        """ The search_string should be 'all' if you want whole
            file secondary structure information. If you want
            secondary structure information for a specific,
            residue, include the residue search string here.
        """
        sstruct = [0,0,0,0,0,0,0]     # initialize variables
        with open(self.file_dir, "r") as f:
            for line in f:
                line = line.replace('\n', ' ').replace('\r', '')
                if line.startswith(search_string) == True or search_string == 'all':
                    if line[0] == '#':
                        continue
                    else:
                        if line[len(line)-2] == "T":
                            sstruct[0]+=1
                        elif line[len(line)-2] == "H":
                            sstruct[1]+=1
                        elif line[len(line)-2] == "E":
                            sstruct[2]+=1
                        elif line[len(line)-2] == "B":
                            sstruct[3]+=1
                        elif line[len(line)-2] == "I":
                            sstruct[4]+=1
                        elif line[len(line)-2] == "G":
                            sstruct[5]+=1
                        elif line[len(line)-2] == "C":
                            sstruct[6]+=1
        for i in range(len(self.letters)):
            print("Found "+str(sstruct[i])+' '+self.names[i]+' in '+self.filename+'.')
        return sstruct
                            
    # Overall file statistics.
                
    def file_info(self):
        """ Determines the number of frames, unique residues,
            and possible number of secondary structure values
            from the file given.
        """
        print("There is/are " + str(self.get_values()) + " possible secondary structure value(s) in " + self.filename + ".") 
        print("There is/are a total of " + str(self.get_total_residues()) + " residue(s) in " + self.filename + ".")  
        if self.get_frames == 'error':
            print("WARNING. Frames may be missing from "+self.filename+" for certain residues.")
        else:
            print("There is/are a total of " + str(self.get_frames()) + " frame(s) in " + self.filename + " for each residue.")  
        
        self.get_sstruct('all') 
    
    # Determine possible values for secondary structures.      
    def get_values(self):
        with open(self.file_dir, 'r') as f:
            values = 0
            for line in f:
                if line[0] != "#": 
                    values+=1
        return values
        
    # Determine number of residues total.
    def get_total_residues(self):
        residues = 0
        for i in range(len(self.sr)):
            if type(self.sr[i]) == list:
                residues += len(self.sr[i])
        return residues
    
    # Determine number of frames.
    def get_frames(self):
        values = self.get_values()
        residues = self.get_total_residues()
        frames = int(values/residues)
        if values%residues != 0:
            frames = "error"
            return frames
        else:
            return frames
    
    # Determine how many times a residue changes its secondary structure
    def get_bitflips(self, full_id):
        flips = 0
        first = True
        with open(self.file_dir, "r") as f:
            for line in f:
                line = line.replace('\n', ' ').replace('\r', '')
                if line.startswith(full_id) == True:
                    if first == True:
                        c_line = line
                        first = False
                    else:
                        if line[len(line)-2] != c_line[len(c_line)-2]:
                            flips+=1
                            c_line = line
        return flips
                       
    # Determine the longest amount of time a residue had a given structure
    def longest_sstruct(self, full_id, sstruct_letter):
        """ With a secondary structure letter code as input,
            this code will determine how long the residue
            spent in that secondary structure before changing
            into a different secondary structure.
        """
        res_frames = self.get_res_frames(full_id)
        status = 'first'
        counter = 1
        frame = -1
        stat_list = []
        with open(self.file_dir, "r") as f:
            for line in f:
                line = line.replace('\n', ' ').replace('\r', '')
                if line.startswith(full_id) == True:
                    frame+=1
                    if status == 'first' and line.endswith(sstruct_letter+' ') == True:
                        status = 'middle'
                    elif status == 'middle':
                        if line.endswith(sstruct_letter+' ') == True:
                            counter+=1
                        elif line.endswith(sstruct_letter+' ') == False:
                            stat_list.append(counter)
                            counter = 1
                            status = 'first'
                    if frame == res_frames-1:
                        if status == 'middle':
                            stat_list.append(counter) 
        return stat_list

    def analyse_stat_list(self, stat_list, name_index):
        try:
            mode = statistics.mode(stat_list)
        except statistics.StatisticsError:
            mode = 'none'
        try:
            mean = statistics.mean(stat_list)
            mean = '%.2f' % mean
        except statistics.StatisticsError:
            mean = 'none'
        try:
            median = statistics.median(stat_list)
        except statistics.StatisticsError:
            median = 'none'
        print('Residue spent a maximum of '+str(max(stat_list))+' frame(s) as secondary structure ' +self.names2[name_index])
        print('Residue spent a minimum of '+str(min(stat_list))+' frame(s) as secondary structure ' +self.names2[name_index])
        if mean != 'none':
            print('Residue spent an average of '+str(mean)+' frame(s) as secondary structure ' +self.names2[name_index])
        else:
            print('There is no mean for this secondary structure.')
        if mode != 'none':
            print('The mode was '+str(mode)+' for frames spent as secondary structure '+self.names2[name_index])
        else:
            print('There is no mode for this secondary structure.')
        if median != 'none':
            print('The median was '+str(median)+' for frames spent as secondary structure '+self.names2[name_index])
        else:
            print('There is no median for this secondary structure.')
        print()
                    
    # Find how many frames there are for a given residue
    def get_res_frames(self, full_id):
        frames = 0
        with open(self.file_dir, "r") as f:
            for line in f:
                line = line.replace('\n', ' ').replace('\r', '')
                if line.startswith(full_id) == True:
                    frames+=1
        return frames
            
    # Get residue specific stats
    def res_stats(self, full_id):
        print()
        sstruct_list = self.get_sstruct(full_id)
        res_frames = self.get_res_frames(full_id)
        print()                    
        print("Residue has "+str(res_frames)+" frames in "+self.filename+'.')
        print()
        for i in range(len(sstruct_list)):
            if sstruct_list[i] != 0:
                percent = sstruct_list[i]/res_frames*100
                print("Residue spent "+str("%.2f" % percent)+"% of the time as secondary structure "+self.names2[i])
                self.analyse_stat_list(self.longest_sstruct(full_id, self.letters[i]), i)
        flips = self.get_bitflips(full_id)
        print("Residue changed its secondary structure "+str(flips)+" time(s).")   
        print()    
    
 
    
    
#############################################################################
#### outside of main class ##################################################
#############################################################################

# Get the name for the test

def get_name():
    name = input("Enter the name of your simulation: ")
    if name == "q":
        return 'q'
    else:
        return name
        
# Get file directory 

def get_dir():
    f_dir = input("Enter the full path of the file you are interested in (ex: /media/jgarne01/Extra Drive 1/ProP-files/R488I-0.50M/steps1-4.tml): ")
    if f_dir == 'q':
        return 'q'
    elif os.path.isfile(f_dir) != True:
        print("No such file in the given directory. Try again or type \"q\" to quit.")
        return 1
    else:
        return f_dir

      
    







    
