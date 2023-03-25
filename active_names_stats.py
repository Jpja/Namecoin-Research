import os
os.chdir(os.path.dirname(__file__))

import csv
file = open("active_names_2023_03_24.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()

#0: block height
#1: date
#2: name
#3: value(s) .. add also updated values that may be in #4, .., #N
for i in range(len(data)-1):
  for j in range(len(data[i])-1):
    if j >= 4:
      data[i][3] += ' -> ' + data[i][j]


groups = ['-', '2011-', '2012-', '2013-', '2014-', '2015-']


# Num of records overall
for group in groups:
  count = 0
  for row in data:
    if group in row[1]:
      count += 1
  print('Name records ' + group + ': ' + str(count))      
print()


# Num of records d/
for group in groups:
  count = 0
  for row in data:
    if group in row[1]:
      if len(row[2]) >= 2 and row[2][0:2] == 'd/':
        count += 1
      #else:
        #print(row[1] + '   ' + row[2] + '   ' + row[3])
  print('d/ ' + group + ': ' + str(count))
print()
  
  
# Num of records by namespace  
for group in groups:
  namespace = {}  
  for row in data:
    if group in row[1]:
      key = ''
      if '/' in row[2]:
        key = row[2].split('/')[0]
      if key in namespace.keys():
        namespace[key] += 1
      else:
        namespace[key] = 1
  print('Namespaces ' + group + ': ' + str(namespace))
print()
    
    
# Punycode subset
for group in groups:
  count = 0
  for row in data:
    if group in row[1]:
      if 'xn--' in row[2].lower():
        count += 1
        #print(row[1] + '   ' + row[2] + '   ' + row[3])
  print('xn-- ' + group + ': ' + str(count))
print()
    

# Keywords
# (look out for false positives)
keys = ['jpg', 'jpeg', 'png', 'gif', 'img', 'image', 'photo', 'mov', 'mp4', 'avi', 'youtu', 'art', 'nft', 'token'] 
for group in groups:
  count = 0
  for row in data:
    if group in row[1]:
      if any([x in row[3].lower() for x in keys]):
        count += 1
        #print(row[1] + '   ' + row[2] + '   ' + row[3])
  print('Keywords ' + group + ': ' + str(count))
print()