def find_substring(string, substring):
    substring_length = len(substring)    
    def recurse(locations_found, start):
        location = string.find(substring, start)
        if location != -1:
            return recurse(locations_found + [location], location+substring_length)
        else:
            return locations_found
    return recurse([], 0)

COMPFILE = open("Compiled_Forms.tex",'w+')

DATABASE = open("Database_Andrea.csv",'r')

for j in DATABASE:
    EXTRACTED = []
    ends = find_substring(j,",")
    #print ends
    toappend = ""
    for i in range(0,ends[0]):
        toappend = toappend + j[i]
    EXTRACTED.append(toappend)
    toappend = ""
    for i in range(ends[1]+1,ends[2]):
        toappend = toappend + j[i]
    toappend = toappend + " "
    for i in range(ends[0]+1,ends[1]):
        toappend = toappend + j[i]
    EXTRACTED.append(toappend)
    #print EXTRACTED
    ADJFORM = open("Adjudication_Form.tex",'r')
    for i in ADJFORM:
        towrite = ''
        if i.find('Name:')==0:
            for ip in range(len(i)-1):
                towrite = towrite + i[ip]
            towrite = towrite + '  ' + EXTRACTED[1] + '\n'
        elif i.find('Instrument/Section:')==0:
            for ip in range(len(i)-1):
                towrite = towrite + i[ip]
            towrite = towrite + '  ' + EXTRACTED[0] + '\n'
        else: 
            towrite = i
        COMPFILE.write(towrite)
        
        
    
