#!/usr/bin/env python3

import cgitb
import codecs
import email.policy
import os
import sys

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
print('<title>上传文件</title>')
print('</head>')
print('<body>')
print('<h2>上传文件</h2>')
# 按照内容长度来读取输入，否则在Linux上会读不到EOF，会一直阻塞下去
body = sys.stdin.buffer.read(int(os.environ['CONTENT_LENGTH']))
header = bytes('Content-Type: ' + os.environ['CONTENT_TYPE'] + '\r\n\r\n', encoding='utf-8')
multipart_form_data = header + body
content = email.message_from_bytes(multipart_form_data, policy=email.policy.HTTP)
for x in content.iter_parts():
    basename = os.path.basename(x.get_filename())
    file_path = os.path.join(upload_dir, basename)
    if os.path.exists(file_path):
        print(f'<h3>{basename}</h3><p>文件已存在。</p>')
        continue
    with open(file_path, mode='xb') as f:
        size = f.write(x.get_content())
        print(f'<h3>{basename}</h3><p>{size}字节已写入。</p>')
print('<p><a href="/">继续上传</a></p>')
print('<p><a href="file-manager.py">文件管理</a></p>')
print('<details>')
print('<p><h3>as_bytes()</h3>', str(content.as_bytes()).replace(r'\r\n', r'\r\n<br>'), '</p>')
print('<p><h3>is_multipart()</h3>', content.is_multipart(), '</p>')
print('<p><h3>items()</h3>', content.items(), '</p>')
print('<hr><h2>iter_parts()</h2>')
for x in content.iter_parts():
    print('<h3>', os.path.basename(x.get_filename()), '</h3>')
    print('<p><h4>', x.get_content_type(), '</h4>x:', str(x).replace('\r\n', '\r\n<br>'), '</p>')
    print('<p>x.get_content():', x.get_content(), '</p>')
print('</details>')
print('</body>')
print('</html>')
