#!/usr/bin/env python
import sys

def find_substring(string,substring):
    if len(string) == 0 or len(substring)==0:
        return []
    substring_length = len(substring)    
    def recurse(locations_found, start):
        location = string.find(substring, start)
        if location != -1:
            return recurse(locations_found + [location], location+substring_length)
        else:
            return locations_found
    return recurse([],0)

def find_characteristics(first):
    pos = find_substring(first,",")
    start = 0
    l = []
    for i in pos:
        aux = ""
        for j in range(start,i):
            aux += first[j]
        l.append(aux)
        start = i+1
    return l

def main(placements,database):
    d = open(database,"r")
    p = open(placements,"r")
    
    name = database+"_filled.csv"
    fd = open(name,"w")
    
    charsd = d.readline()
    charsp = p.readline()
    
    ld = find_characteristics(charsd)
    lp = find_characteristics(charsp)
    
    data = []
    for line in d:
        l = find_characteristics(line)
        data.append(l)

    tofill = []
    for line in p:
        l = find_characteristics(line)
        tofill.append(l)

    print "The following characteristics are to be filled:"
    mapp = []
    posa = 0
    for cha in lp:
        pose = 0
        for che in ld:
            a = find_substring(che,cha)
            if len(a) != 0:
                print cha,"found in",che
                mapp.append([posa,pose])
            pose += 1
        posa += 1
        
    print "Now filling data for students"
    which = []
    for student in data:
        count = 0
        for otherstudent in tofill:
            a = find_substring(otherstudent[0],student[0])
            b = find_substring(otherstudent[0],student[1])
            if len(a)!=0 and len(b)!=0:
                print "Filling data for",otherstudent[0]
                for c in mapp:
                    student[c[1]] = otherstudent[c[0]]
                which.append(count)
            count += 1
          
    for w in range(len(tofill)):
        if w not in which:
            print "Warning:",tofill[w][0],"student not found"
    
    for line in data:
        towrite = ""
        for ex in line:
            towrite += str(ex) + ","
        towrite += "\n"
        fd.write(towrite)
                
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
