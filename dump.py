import requests
import subprocess
import sys
import time

res = requests.get('http://10.250.0.27:9200/_cat/indices?v')
res_str = res.content.decode('utf-8')
idx_split = res_str.split()
del idx_split[0:12]
idx_name = idx_split[::10]

timestr = time.strftime("%d_%m_%Y")
log = open('dumplog_' + timestr + '.txt', 'a')

# run mapping dump
for i in idx_name:
    process_map = subprocess.Popen(['elasticdump', '--input=http://10.250.0.27:9200/' + i,
                                    '--output=http://10.250.0.26:9200/' + i, '--type=mapping'],
                                   universal_newlines=True, stdout=log, stderr=log)
    with open('dumplog_' + timestr + '.txt', 'a') as sys.stdout:
        print(process_map.args)
    process_map.communicate()
    log.flush()

# run data dump
for i in idx_name:
    process_data = subprocess.Popen(['elasticdump', '--input=http://10.250.0.27:9200/' + i,
                                     '--output=http://10.250.0.26:9200/' + i, '--type=data'],
                                    universal_newlines=True, stdout=log, stderr=log)
    with open('dumplog_' + timestr + '.txt', 'a') as sys.stdout:
        print(process_data.args)
    process_data.communicate()
    log.flush()
