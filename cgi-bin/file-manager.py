#!/usr/bin/env python3

import cgitb
import codecs
import os
import sys
import time
from urllib.parse import parse_qs

upload_dir = 'upload/'
cgitb.enable()
if not os.path.lexists(upload_dir):
    os.mkdir(upload_dir)
# sys.excepthook = lambda exception_type, value, tb: print('<p>', html.escape(str(exception_type)), '<br>', value, '<br>', html.escape(str(tb)), '</p></body></html>')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print('Content-type: text/html; charset=utf-8', end='\r\n')
print(end='\r\n')  # 空行，告诉服务器结束头部
print('<!DOCTYPE html>')
print('<html lang="zh">')
print('<head>')
print('<meta charset="utf-8">')
print('<title>文件管理</title>')
print('</head>')
print('<body>')
print('<h2>文件管理</h2>')
query = ''
deleted = []
non_existent = []
if os.environ.get('REQUEST_METHOD') == 'POST':
    try:
        query = parse_qs(input())
        for filename in query['filename']:
            basename = os.path.basename(filename)
            if os.path.exists(upload_dir + basename):
                os.remove(upload_dir + basename)
                deleted.append(basename)
            else:
                non_existent.append(basename)
    except EOFError:
        pass  # 没有POST消息体，即没有要删除的文件
print('<form method="post">')
print('<table border="1"><thead><tr><td></td><td><b>文件名</b></td><td><b>大小</b></td><td><b>上传时间</b></td></tr></thead><tbody>')
with os.scandir(upload_dir) as file_list:
    for entry in file_list:
        print(f'<tr><td><input type="checkbox" name="filename" value="{entry.name}"></td>'
              f'<td><a href="/{upload_dir}{entry.name}">{entry.name}</a></td>'
              f'<td>{entry.stat().st_size}字节</td>'
              f'<td>{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entry.stat().st_mtime))}</td></tr>')
print('</tbody></table>')
print('<br><button>删除选中文件</button>')
print('</form>')
if len(deleted) != 0:
    print(f'<p>以下文件已删除：{deleted}</p>')
if len(non_existent) != 0:
    print(f'<p>以下文件不存在，无需删除：{non_existent}</p>')
print('<p><a href="../index.html">上传文件</a></p>')
if query != '':
    print(f'<details><p>{query}</p></details>')
print('</body>')
print('</html>')
