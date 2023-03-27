"""
Generates a .csv file of all names that were registered before a threshold date and have not expired since.
  Format height,YYYY-MM-DD,name,value1[, .., valueN]
The script makes rpc calls to Namecoin Core.
It loops through all blocks to collect all name operations.
It then looks up each name and filters out names that never expired.
"""


threshold_date = '2015-12-31'


from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import csv
from datetime import datetime
from datetime import timezone

import os
os.chdir(os.path.dirname(__file__))

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%("123", "123"))

start = 0
#maxblock = 20000 #for testing
maxblock = rpc_connection.getblockcount()

names = set() #set of all names
ts = [0] * (maxblock+1) #list of block timestamps

#for stats
year = '2011'
name_count = 0

updates = {}

#Loop through blocks
#  collect every 'name_firstupdate' and 'name_update'
print('Looping all blocks to collect name operations')
for i in range(start, maxblock+1):
  blockhash = rpc_connection.getblockhash(i)
  x = rpc_connection.getblock(blockhash, 2)
  
  ts[i] = datetime.fromtimestamp(x['time'], tz=timezone.utc) #YYYY-MM-DD
  ts[i] = ts[i].strftime("%Y-%m-%d")
  
  if ts[i][0:4] != year:
    print('  Name registrations in ' + year + ': ' + str(name_count))
    year = ts[i][0:4]
    name_count = 0
    
  for y in x["tx"]:
    for z in y["vout"]:
      if 'nameOp' in z["scriptPubKey"]:
        nameop = z["scriptPubKey"]['nameOp']
        if 'name' in nameop:
          name = nameop['name']
          type = 0
          if nameop['op'] == 'name_firstupdate':
            type = 1
            name_count += 1
          if nameop['op'] == 'name_update':
            type = 2
          value = ''
          if 'value' in nameop:
            value = nameop['value']
          if name not in updates.keys():
            updates[name] = []
          if type == 1 or type == 2:
            updates[name].append([x['height'], type, value])
            
          
#For each name
#  add to name history only if still active and registered before threshold date
print('Looping all names to get name history')
name_history = []
for name in updates:

  if updates[name][-1][0] < maxblock - 36000:
    #last update more than 36k blocks ago == expired -> dismiss
    continue
    
  after_threshold = False
  for op in updates[name]:
    if op[1] == 1 and ts[op[0]] > threshold_date:
      #firstupate happened after the threshold -> dismiss
      after_threshold = True
      break
  if after_threshold == True:
    continue
  
  #collect data for name
  name_info = ['', '', name] #block, ts of last firstupdate before threshold, name, value1, .. , valueN
  values = []
  for op in updates[name]:
    if ts[op[0]] > threshold_date:
      if name_info[0] == '': #sanity check
        print('  No reg date for ' + name)
      break
    if op[1] == 1: #new firstupdate -> reset values
      name_info[0] = op[0]
      name_info[1] = ts[op[0]]
      values = []
      values.append(op[2])
    if op[1] == 2: #new update -> add value if it is changed
      if op[2] != values[-1]:
        values.append(op[2])
  name_info.extend(values)
  name_history.append(name_info)
  
          
print('Sorting by date')
name_history.sort(key=lambda x: int(x[0]))


file = 'active_names_' + ts[maxblock].replace('-','_') + '.csv'
print('Saving ' + file)
with open(file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(name_history)