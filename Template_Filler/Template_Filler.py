#!/usr/bin/env python
import sys,os

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

def seek_and_destroy(template,keys,data,permissive=False):
    tmp_arg_mrk = "////"
    com_char = '%'
    special_chars = ['_','&']
    template_file = open(template,"r")
    filled_template = ""
    has_empty = False
    for template_line in template_file:
        if template_line.find(com_char)==0:
            continue
        add_lnj = False
        template_args = find_substring(template_line,tmp_arg_mrk)
        line = template_line
        if len(template_args)%2 != 0:
            print '\33[31mError\33[0m: Template key merker error in:',template_line,'\n'
            print 'The correct usage is:'+tmp_arg_mrk+'Some Template Argument'+tmp_arg_mrk
            sys.exit()
        for index in range(len(template_args)/2):
            template_key = template_line[(template_args[2*index]+len(tmp_arg_mrk)):template_args[2*index+1]]
            template_pattern = tmp_arg_mrk+template_key+tmp_arg_mrk
            try:
                line = line.replace(template_pattern,data[keys[template_key]])
            except:
                print "\33[31mError\33[0m: Template key:",template_key,"was not found in database"
                sys.exit()
            #print "Replacing template pattern:",template_pattern,"with template argument:",data[keys[template_key]]
            #print line
                    
            has_empty = (data[keys[template_key]] == '')
        for char in special_chars:
            line = line.replace(char,str('\\'+char))
        filled_template += line
    if has_empty:
        wrn_msg = "\33[95mWarning\33[0m: "
        wrn_msg += "data structure: "+str(data)+" has an empty template argument"
        if not permissive:
            wrn_msg += ", skkiped"
            filled_template = ""
        else:
            wrn_msg += ", written with missing arguments"
        print wrn_msg
    return filled_template

def main(template,database):
    ##
    ## Here we read the first line, which has the characteristics and look for them
    ## We then create a dictionary 'keys' that maps the characteristic to its column
    ##
    
    students = open(database,"r")
    charsd = students.readline()
    ld = find_characteristics(charsd)
    keys = {}
    for i in range(len(ld)):
        keys[ld[i]] = i
    
    ##
    ## Here we loop over the database of students 
    ## the seek_and_destroy method looks inside the template for the attributes
    ## in keys and if it finds them it will overwrite them to the students attributes.
    ##
    
    name = database+"_"+template
    students_labels = open(name,"w")
    for student in students:
        student_characteristics = find_characteristics(student)
        #print "\33[32mWorking on\33[0m:",student_characteristics[keys['First Name']],student_characteristics[keys['Last Name']]
        student_label = seek_and_destroy(template,keys,student_characteristics)
        # if (student_characteristics[keys['Ensemble 1st Cycle']].find('StringOrchestra')==0):
            # students_labels.write(student_label)
        students_labels.write(student_label)
            
if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
