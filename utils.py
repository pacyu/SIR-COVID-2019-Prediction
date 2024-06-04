import time, json, requests
import numpy as np
import pandas as pd

date = str(time.time() * 100).replace('.', '_')
url = 'https://voice.baidu.com/newpneumonia/get?target=trend&isCaseIn=0&stage=publish&callback=jsonp_%s' % str(date)
r = requests.get(url)
res = r.text.replace('jsonp_' + date, '')

par_res = json.loads(res[1:-2])
data = par_res['data']
group_by_date = {'日期': data[0]['trend']['updateDate'], '确诊': [], '治愈': [], '死亡': [], '新增确诊': []}
for _ in data:
    for group in _['trend']['list']:
        if group['name'] == '确诊':
            if len(group['data']) < 189:
                for _ in range(189 - len(group['data'])):
                    group['data'].append(0)
            group_by_date['确诊'].append(np.array(group['data']))
        elif group['name'] == '治愈':
            if len(group['data']) < 189:
                for _ in range(189 - len(group['data'])):
                    group['data'].append(0)
            group_by_date['治愈'].append(np.array(group['data']))
        elif group['name'] == '死亡':
            if len(group['data']) < 189:
                for _ in range(189 - len(group['data'])):
                    group['data'].append(0)
            group_by_date['死亡'].append(np.array(group['data']))
        elif group['name'] == '新增确诊':
            if len(group['data']) < 189:
                for _ in range(189 - len(group['data'])):
                    group['data'].append(0)
            group_by_date['新增确诊'].append(np.array(group['data']))
group_by_date['确诊'] = np.sum(group_by_date['确诊'], axis=0,)
group_by_date['治愈'] = np.sum(group_by_date['治愈'], axis=0)
group_by_date['死亡'] = np.sum(group_by_date['死亡'], axis=0)
group_by_date['新增确诊'] = np.sum(group_by_date['新增确诊'], axis=0)
df = pd.DataFrame(group_by_date)
df.to_csv('CoVID_19_China.csv', index=False, encoding='utf8')
