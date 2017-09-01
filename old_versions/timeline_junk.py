    # SEGMENT ONE
    segment1 = input("Enter the first segment ID. Make sure the format (e.g. capitalization) is the same as what is in your file. Example PROA: ")
    if segment1 == "q":
        return 'q'
    else:
        AA1 = input("Enter the amino acid range for the first segment, separated by a hyphen. Do not put spaces. It is assumed that each amino acid increases the range by 1. The range can start from any positive integer or zero. Examples 1-5, 0-20, 5-34: ")
        if AA1 == 'q':
            return 'q'
        else:
            hyphen = AA1.index('-')
            first = int(AA1[0:hyphen])
            last = int(AA1[hyphen+1:len(AA1)])
            AA1 = list(range(first, last+1))
                
    # SEGMENT TWO    
    segment2 = input("Enter the second segment ID. Type \"none\" if there is only one segment: ")
    if segment2 == "q":
        return 'q'
    elif segment2 == 'none':
        AA2=AA3=AA4=AA5=segment2=segment3=segment4=segment5 = 'none'
        return [segment1, AA1, segment2, AA2, segment3, AA3, segment4, AA4, segment5, AA5]
    else:
        AA2 = input("Enter the amino acid range for the second segment: ")
        if AA2 == 'q':
            return 'q'
        else:
            hyphen = AA2.index('-')
            first = int(AA2[0:hyphen])
            last = int(AA2[hyphen+1:len(AA2)])
            AA2 = list(range(first, last+1))
    # SEGMENT THREE
    segment3 = input("Enter the third segment ID. Type \"none\" if there are only two segments: ")
    if segment3 == "q":
        return 'q'
    elif segment3 == 'none':
        AA3=AA4=AA5=segment3=segment4=segment5 = 'none'
        return [segment1, AA1, segment2, AA2, segment3, AA3, segment4, AA4, segment5, AA5]
    else:
        AA3 = input("Enter the amino acid range for the third segment: ")
        if AA3 == 'q':
            return 'q'
        else:
            hyphen = AA3.index('-')
            first = int(AA3[0:hyphen])
            last = int(AA3[hyphen+1:len(AA3)])
            AA3 = list(range(first, last+1))    
            
    # SEGMENT FOUR
    segment4 = input("Enter the fourth segment ID. Type \"none\" if there are only three segments: ")
    if segment4 == "q":
        return 'q'
    elif segment4 == 'none':
        AA4=AA5=segment4=segment5 = 'none'
        return [segment1, AA1, segment2, AA2, segment3, AA3, segment4, AA4, segment5, AA5]
    else:
        AA4 = input("Enter the amino acid range for the fourth segment: ")
        if AA4 == 'q':
            return 'q'
        else:
            hyphen = AA4.index('-')
            first = int(AA4[0:hyphen])
            last = int(AA4[hyphen+1:len(AA4)])
            AA4 = list(range(first, last+1))   
                     
    # SEGMENT FIVE
    segment5 = input("Enter the fifth segment ID. Type \"none\" if there are only four segments: ")
    if segment5 == "q":
        return 'q'
    elif segment5 == 'none':
        AA5=segment5 = 'none'
        return [segment1, AA1, segment2, AA2, segment3, AA3, segment4, AA4, segment5, AA5]
    else:
        AA5 = input("Enter the amino acid range for the fifth segment: ")
        if AA5 == 'q':
            return 'q'
        else:
            hyphen = AA5.index('-')
            first = int(AA5[0:hyphen])
            last = int(AA5[hyphen+1:len(AA5)])
            AA5 = list(range(first, last+1))
            return [segment1, AA1, segment2, AA2, segment3, AA3, segment4, AA4, segment5, AA5]


