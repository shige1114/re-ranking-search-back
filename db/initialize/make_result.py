import os
import datetime
import json
import pandas as pd

DATA_DIR = 'data'

def makeDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def makeSearchResults():
    response_filename = os.path.join('english.json')
    response_file = open(response_filename, 'r')
    response_json = response_file.read()
    response_tmp = json.loads(response_json)
    ymd = response_tmp['snapshot_ymd']
    response = response_tmp['response']
    results = []
    cnt = 0
    for one_res in range(len(response)):
        if 'items' in response[one_res] and len(response[one_res]['items']) > 0:
            for i in range(len(response[one_res]['items'])):
                cnt += 1
                display_link = response[one_res]['items'][i]['displayLink']
                title        = response[one_res]['items'][i]['title']
                link         = response[one_res]['items'][i]['link']
                snippet      = response[one_res]['items'][i]['snippet'].replace('\n', '')
                ad = response[one_res]['items'][i]['ad']
                results.append({'ymd': ymd, 'no': cnt, 'display_link': display_link, 'title': title, 'link': link, 'snippet': snippet,'ad':0,'click':0,'view':0})
                print(results)
    save_results_dir = os.path.join(DATA_DIR, 'results')
    makeDir(save_results_dir)
    df_results = pd.DataFrame(results)
    # df_results.to_excel(os.path.join(save_results_dir, 'results_' + ymd + '.xlsx'), sep='\t', index=False, columns=['ymd', 'no', 'display_link', 'title', 'link', 'snippet','ad','click','view'])
    df_results.to_excel(os.path.join(save_results_dir, 'results_' + ymd + '.xlsx'), index=False, columns=['ymd', 'no', 'display_link', 'title', 'link', 'snippet', 'ad', 'click', 'view'])

if __name__ == '__main__':

    makeSearchResults()