import json
import sqlite3
import numpy as np
from os.path import join
import datetime

def clean_url(s):
    if s[:4] != 'http':
        return False
    else:
        root = s.split('/')[2]
        if root[:4] == 'www.':
            root = root[4:]
        return root

def date_from_webkit(webkit_timestamp):
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    return epoch_start + delta

def process_history(data_dir,f):
    conn = sqlite3.connect(join(data_dir,f))
    c = conn.cursor()

    if '.sql' not in f.lower():
        c.execute('SELECT * FROM urls')
    else:
        c.execute('SELECT * FROM moz_places')

    data = c.fetchall()
    id_to_url = dict(zip([p[0] for p in data],[p[1] for p in data]))

    if '.sql' not in f.lower():
        c.execute('SELECT * FROM visits')
    else:
        c.execute('SELECT * FROM moz_historyvisits')

    data = c.fetchall()
    data = np.array(data)

    if '.sql' not in f.lower():
        ids = data[:,0]
        source_ids = data[:,3]
        url_ids = data[:,1]
        times = data[:,2]
    else:
        ids = data[:,0]
        source_ids = data[:,1]
        url_ids = data[:,2]
    id_to_url_id = dict(zip(ids,url_ids))

    nodes = {}
    edges = {}

    for source_id,target_id in zip(source_ids,url_ids):
        try:
            if source_id != 0:
                source_id = id_to_url_id[source_id]
                source_url = clean_url(id_to_url[source_id])
                target_url = clean_url(id_to_url[target_id])
                if source_url != target_url:
                    if source_url != False and target_url != False:
                        if 'google' not in source_url and 'google' not in target_url:
                            if source_url in nodes:
                                nodes[source_url] += 1
                            else:
                                nodes[source_url] = 1
                            if target_url in nodes:
                                nodes[target_url] += 1
                            else:
                                nodes[target_url] = 1
                            key = ' '.join(sorted([source_url,target_url]))
                            if key in edges:
                                edges[key] += 1
                            else:
                                edges[key] = 1
        except:
            print 'err on',source_id,target_id

    url_to_node_id = {}
    nodes_list = []
    edges_list = []
    for key in nodes:
        url_to_node_id[key] = len(url_to_node_id)
        nodes_list.append({'name':key,'score':nodes[key]})

    for edge_pair in edges:
        source_url,target_url = edge_pair.split(' ')
        source_id = url_to_node_id[source_url]
        target_id = url_to_node_id[target_url]
        edges_list.append({'source':source_id,'target':target_id,'value':edges[edge_pair]})

    data = {'nodes':nodes_list,'links':edges_list}
    # json.dump(data,open('steph_firefox.json','wb'))
    return json.dumps(data)
