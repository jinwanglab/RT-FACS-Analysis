# import library
import csv
import math
import os

# define global variables
v=[]
result=[]
IntvP=[]
IntvF=[]
l=[0,1]

# define functions
def average(num):
	l=0	
	lsum=0.0
	if len(num)==0: return 0
	while l < len (num):
		lsum = lsum + num[l]
		l += 1
	return lsum/l

def stdev(num):
	k=0
	ksum=0.0
	ave=average(num)
	if len(num) ==0: return 0
	while k < len (num):
		ksum = ksum + (abs(num[k]-ave))**2
		k += 1
	return math.sqrt(ksum/(k-1))

# Open a csvfile, calculate ratio from the two columns, store into a new list
def ratio(dir):
        with open(dir, 'rb') as csvfile:
                numbers = csv.reader(csvfile)
                for row in numbers:
                        for col in xrange(len(row)):
                                if row[col] == ' "PE-A"': FI=col
                                elif row[col] == ' "Pacific Blue-A"': PA=col
                                else: continue
                        break
                v[:]=[]
                IntvP[:]=[]
                IntvF[:]=[]
                for row in numbers:
                        if float(row[PA]) > 0 and float(row[FI]) > 0 :
                                r = float(row[PA])/float(row[FI])
                                v.append(r)
                                IntvP.append(float(row[PA]))
                                IntvF.append(float(row[FI]))
        csvfile.close()
        return v					

# Statistical analysis of the ratio list, confine the range to a statistical meaningful set of data
def stat():
        i=0
        rang=4
        v.sort()

        if len(v) <= 1:
                result.append(1)
                result.append(1)
                result.append(1)
                return
        while l[i+1] != l[i]: 
                ave=average(v)
                std=stdev(v)
                for x in v:
                        if x < ave - rang * std or x> ave + rang * std:
                                v.remove(x)
                i += 1	
                l.append(len(v))

        result.append(ave)
        result.append(std)
        result.append(len(v))
        print len(v),len(IntvP),len(IntvF)
        for j in xrange(len(v)):
                try: x=IntvP[j]/IntvF[j]
                except: break
                if x < ave - rang * std or x > ave+rang*std:
                        IntvP.remove(IntvP[j])
                        IntvF.remove(IntvF[j])
      
        return result

# Main program begins

# Get the file directory

#print "Enter directory: (enter '.' for current directory)"
#path = raw_input()

path = '.'

# Create a result file for storage
fw = open ('result.txt', 'w+')
fw.write("file\taverage\tstdev\tN\tSEM\tGreen\tBlue\n")
fw.close()

# Process all csv files in the directory
for files in os.listdir(path):
        if files.endswith(".csv"):
                ratio(files)
                print stat()
                print average(IntvP),average(IntvF),len(IntvP)
# Write the output to the result.txt file
                fw = open ('result.txt', 'ab')
                fw.write(files)
                fw.write('\t')
                fw.write(str(round(result[0],4)))
                fw.write('\t')
                fw.write(str(round(result[1],4)))
                fw.write('\t')
                fw.write(str(result[2]))
                fw.write('\t')
                fw.write(str(round(result[1]/(math.sqrt(result[2])),5)))
                fw.write('\t')
                fw.write(str(average(IntvF))+'\t'+str(average(IntvP)))
                fw.write('\n')
                fw.close()
                result[:]=[]


