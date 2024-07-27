import json
import pymysql
import json, pandas as pd
import numpy as np
import os
from tqdm import tqdm
import time

# MySQL 데이터베이스 연결
conn=pymysql.connect(host='127.0.0.1',user='root',password='012345',db='sue',charset='utf8mb4')

# 뉴스 업로드
while True:
    ######################################## KBS 뉴스업로드 ########################################
    KBS_news = [os.path.join('D:/VS_code/KBS_news', f) for f in tqdm(os.listdir('D:/VS_code/KBS_news')) if f.endswith('.json')]
    if (len(KBS_news) == 0): time.sleep(3)

    # JSON 파일 읽기
    with open(KBS_news[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 커서 생성
    cur = conn.cursor()
    print('%s',data['field'])
    cur.execute("SELECT id FROM blog_category WHERE name = %s", (data['field'],))
    field_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM blog_news WHERE name = %s", (data['company'],))
    company_id = cur.fetchone()[0]

    # 데이터 삽입
    cur.execute("INSERT INTO blog_post (title, text_short, time, image, field_id, company_id, url, text_long, text_middle, writer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['title'], data['text_short'], data['time'], data['image'], field_id, company_id, data['url'], data['text_long'], data['text_middle'], data['writer']))
    
    # 커밋
    conn.commit()
    
    # 저장한 json 파일 삭제
    os.remove(KBS_news[0])

    ######################################## SBS 뉴스업로드 ########################################
    SBS_news = [os.path.join('D:/VS_code/SBS_news', f) for f in tqdm(os.listdir('D:/VS_code/SBS_news')) if f.endswith('.json')]
    if (len(SBS_news) == 0): time.sleep(3)

    # JSON 파일 읽기
    with open(SBS_news[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 커서 생성
    cur = conn.cursor()
    print('%s',data['field'])
    cur.execute("SELECT id FROM blog_category WHERE name = %s", (data['field'],))
    field_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM blog_news WHERE name = %s", (data['company'],))
    company_id = cur.fetchone()[0]

    # 데이터 삽입
    cur.execute("INSERT INTO blog_post (title, text_short, time, image, field_id, company_id, url, text_long, text_middle, writer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['title'], data['text_short'], data['time'], data['image'], field_id, company_id, data['url'], data['text_long'], data['text_middle'], data['writer']))
    
    # 커밋
    conn.commit()
    
    # 저장한 json 파일 삭제
    os.remove(SBS_news[0])

    ######################################## KBS 뉴스업로드 ########################################
    MBC_news = [os.path.join('D:/VS_code/MBC_news', f) for f in tqdm(os.listdir('D:/VS_code/MBC_news')) if f.endswith('.json')]
    if (len(MBC_news) == 0): time.sleep(3)

    # JSON 파일 읽기
    with open(MBC_news[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 커서 생성
    cur = conn.cursor()
    print('%s',data['field'])
    cur.execute("SELECT id FROM blog_category WHERE name = %s", (data['field'],))
    field_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM blog_news WHERE name = %s", (data['company'],))
    company_id = cur.fetchone()[0]

    # 데이터 삽입
    cur.execute("INSERT INTO blog_post (title, text_short, time, image, field_id, company_id, url, text_long, text_middle, writer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['title'], data['text_short'], data['time'], data['image'], field_id, company_id, data['url'], data['text_long'], data['text_middle'], data['writer']))
    
    # 커밋
    conn.commit()
    
    # 저장한 json 파일 삭제
    os.remove(MBC_news[0])

# 연결 종료
conn.close()