#!/usr/bin/env python3

import cgitb
import codecs
import os
import sys
import time
from urllib.parse import parse_qs

upload_dir = 'upload'
cgitb.enable()
if not os.path.lexists(upload_dir):
    # 保存当前umask
    original_umask = os.umask(0)
    # 创建目录，设置权限为775，因为在Linux系统上，运行CGI脚本的用户不是当前用户，而是nobody
    os.mkdir(upload_dir, mode=0o775)
    # 恢复原始umask
    os.umask(original_umask)
# sys.excepthook = lambda exception_type, value, tb: print('<p>', html.escape(str(exception_type)), '<br>', value, '<br>', html.escape(str(tb)), '</p></body></html>')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print('Content-Type: text/html; charset=utf-8', end='\r\n')
print(end='\r\n')  # 空行，告诉服务器结束头部
print('<!DOCTYPE html>')
print('<html lang="zh">')
print('<head>')
print('<meta charset="utf-8">')
print('<title>文件管理</title>')
print('</head>')
print('<body>')
print('<h2>文件管理</h2>')
query = {}
deleted = []
non_existent = []
if os.environ.get('REQUEST_METHOD') == 'POST':
    # 按照内容长度来读取输入，否则在Linux上会读不到EOF，会一直阻塞下去
    body = sys.stdin.buffer.read(int(os.environ['CONTENT_LENGTH']))
    query = parse_qs(body.decode('utf-8'))
    if 'filename' in query:
        for filename in query['filename']:
            basename = os.path.basename(filename)
            file_path = os.path.join(upload_dir, basename)
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted.append(basename)
            else:
                non_existent.append(basename)
print('<form method="post">')
print('<table border="1"><thead><tr><td></td><td><b>文件名</b></td><td><b>大小</b></td><td><b>上传时间</b></td></tr></thead><tbody>')
with os.scandir(upload_dir) as file_list:
    for entry in file_list:
        print(f'<tr><td><input type="checkbox" name="filename" value="{entry.name}"></td>'
              f'<td><a href="/{upload_dir}/{entry.name}">{entry.name}</a></td>'
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
if query != {}:
    print(f'<details><p>{query}</p></details>')
print('</body>')
print('</html>')
