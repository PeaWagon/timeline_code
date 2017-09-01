# Python code to analyze .tml data files from the timeline plugin
# from VMD.

# VERSION 3

# JEN

# Monday 22nd August, 2016

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
    ProP_residues_let = '0MLKRKKVKPITLRDVTIIDDGKLRKAITAASLGNAMEWFDFGVYGFVAYALGKVFFPGADPSVQMVAALATFSVPFLIRPLGGLFFGMLGDKYGRQKILAITIVIMSISTFCIGLIPSYDTIGIWAPILLLICKMAQGFSVGGEYTGASIFVAEYSPDRKRGFMGSWLDFGSIAGFVLGAGVVVLISTIVGEANFLDWGWRIPFFIALPLGIIGLYLRHALEETPAFQQHVDKLEQGDREGLQDGPKVSFKEIATKYWRSLLTCIGLVIATNVTYYMLLTYMPSYLSHNLHYSEDHGVLIIIAIMIGMLFVQPVMGLLSDRFGRRPFVLLGSVALFVLAIPAFILINSNVIGLIFAGLLMLAVILNCFTGVMASTLPAMFPTHIRYSALAAAFNISVLVAGLTPTLAAWLVESSQNLMMPAYYLMVVAVVGLITGVTMKETANRPLKGATPAASDIQEAKEILVEHYDNIEQKIDDIDHEIADLQAKRTRLVQQHPRIDE'
    res_desc = { 'non-polar, aliphatic': ['G', 'A', 'L', 'I', 'P'], 'aromatic': ['F', 'Y', 'W'], 'polar, non-charged': ['S', 'T', 'C', 'M', 'N', 'Q'], 'positively charged': ['K', 'R', 'H'], 'negatively charged': ['D', 'E'] }
    
    def __init__(self, name, file_dir, filename, sr, PCT):
        self.name = name
        self.file_dir = file_dir
        self.filename = filename
        self.sr = sr
        self.PCT = PCT
    
    # Determine whether file describes ProP c-terminus or not
    
    def is_ProP(self):
        assertion = input("Is "+self.filename+" a ProP c-terminus file? (Y/n) ")
        if assertion == 'q':
            return 'q'
        elif assertion == 'Y':
            self.PCT = True
            query = self.update_tml()       # ask whether to update tml file
            while query == 3:
                query = self.update_tml()
            if query == 'q':
                return 'q'
            return 1
        elif assertion == 'n':
            self.PCT = False
            return 2
        else:
            print("Invalid input. Try again or type \"q\" to quit.")
            return 3
   

    # ask whether to update tml file
    def update_tml(self):
        print()
        query = input("Would you like to update the tml file with actual ProP residue ranges? (Y/n) ")
        if query == 'q':
            return 'q'
        elif query == 'Y':
            print("The file will now be updated.")
            self.new_tml()          # make new tml file with updated residues
            self.get_info_2()       # update self.sr with new values
            self.print_sr()         # print new values
            return 1
        elif query == 'n':
            return 2
        else:
            print("Invalid input. Try again or type \"q\" to quit.")
            return 3
            
    # update tml file 
    def new_tml(self):
        i_dir = self.file_dir[:self.file_dir.rindex('/')+1]
        temp_file = i_dir+'temp'+self.filename
        with open(self.file_dir, 'r') as f, open(temp_file, 'w') as out:
            for line in f:
                if line.startswith('#'):
                    out.write(line)
                else:
                    residue = int(line[:line.index(' ')])
                    if residue > 36:
                        residue-=36
                    residue += 464
                    out.write(str(residue)+line[line.index(' '):])
        self.file_dir = temp_file

    
    # pull information for residue and segments from tml file
    
    def get_info_2(self):
        self.sr = []        # clears current state if necessary
        lines = self.get_values()
        line_num = 0 
        first = True
        s=0         # segment index
        r=1         # residue number index
        with open(self.file_dir, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                else:
                    line_num+=1
                    first_space = line.index(' ')
                    second_space = first_space+line[first_space+1:].index(' ')+1
                    last_space = line.rindex(' ')
                    second_last_space = line[:last_space].rindex(' ')
                    segment = line[second_space+1:second_last_space]
                    residue = int(line[:first_space])
                            
                    # normal end condition (end of first frame)
                    if line[second_last_space+1:last_space] != '0':
                        return self.sr
                    
                    # end condition (if only one frame for all residues)
                    elif line_num == lines:
                        
                        if segment in self.sr:
                            self.sr[r].append(residue)
                        else:
                            s+=2
                            r+=2
                            self.sr.append(segment)
                            self.sr.append([residue])
                        return self.sr
                        
                    # start of new segment name    
                    elif first == True:
                        self.sr.append(segment)
                        self.sr.append([residue])
                        first = False
                    
                    # segment is already in sr
                    elif segment in self.sr:
                        self.sr[r].append(residue)
                    
                    # segment is not in sr
                    else:
                        self.sr.append(segment)
                        self.sr.append([residue])
                        s+=2
                        r+=2
                    
    # print info from sr
    
    def print_sr(self):
        print()
        print("This information was found in the file "+self.filename+':')
        for i in range(0, len(self.sr), 2):
            print("Segment "+self.sr[i]+" contains residues "+str(self.sr[i+1][0])+" through "+str(self.sr[i+1][-1])+'.')
        print()
    
    
    # Allow user to get file statistics

    def get_file(self):
        gen_stat = input("Return file statistics? (Y/n) ")
        if gen_stat == "Y":
            print("General file statistics will now be reported for " + self.name + '.')
            print()
            return 1
        elif gen_stat == "n":
            print("General file statistics will be skipped.")
            print()
            return 2 
        elif gen_stat == "q":
            return 'q'
        else:
            print("Invalid input. Try again, or press \"q\" to quit.")
            return 3
    
    # Allow user to choose specific segment/residue IDs

    def get_res(self):
        res_stat = input("Return specific residue statistics? (Y/n) ")
        if res_stat == "Y":
            full_id = self.print_res_stats()
            while full_id == 3:
                full_id = self.print_res_stats()
            if full_id == 'q':
                return 'q'
            else:
                self.res_stats(full_id) # print residue stats
                res_stat = self.next_res()
                while res_stat == 1:
                    full_id = self.print_res_stats()
                    while full_id == 3:
                        full_id = self.print_res_stats()
                    if full_id == 'q':
                        return 'q'
                    else:
                        self.res_stats(full_id)
                        res_stat = self.next_res()
  
        # User does not want residue statistics
        if res_stat == "n":
            print("Residue file statistics will be skipped.")
            return 2
        # User quit
        elif res_stat == "q":
            return 'q'
        # Invalid input
        else:
            print("Invalid input. Try again, or type \"q\" to quit.")
            return 3
    
    def print_res_stats(self):
        # User wants residue statistics
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
        elif query == 'n':
            return 'n'
        elif query == 'Y':
            return 1
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
        if self.get_frames() == 'error':
            print("WARNING. Frames may be missing from "+self.filename+" for certain residues.")
        else:
            print("There is/are a total of " + str(self.get_frames()) + " frame(s) in " + self.filename + " for each residue.")  
        print()
        sstruct_list = self.get_sstruct('all') 
        print()
        for i in range(len(sstruct_list)):
            if sstruct_list[i] != 0:
                percent = sstruct_list[i]/self.get_values()*100
                print("Overall, the residue(s) spent "+str("%.2f" % percent)+"% of the time as secondary structure "+self.names2[i]) 
        print()              
    
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
            return 'error'
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
        if self.PCT == True:
            residue_num = int(full_id[:full_id.index(' ')])
            res_letter = self.ProP_residues_let[residue_num]
            for key in self.res_desc:
                if res_letter in self.res_desc[key]:
                    desc_r = key
            print("This residue is "+res_letter+', which is a '+desc_r+' residue.')
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

# Tests

#def pikachu():
#    chespin = os.getcwd()
#    return chespin






    
