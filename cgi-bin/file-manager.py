import cgitb
import codecs
import os
import sys
from urllib.parse import parse_qs

upload_dir = 'upload/'
cgitb.enable()
if not os.path.lexists(upload_dir):
    os.mkdir(upload_dir)
# sys.excepthook = lambda exception_type, value, tb: print('<p>', html.escape(str(exception_type)), '<br>', value, '<br>', html.escape(str(tb)), '</p></body></html>')
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print('Content-type: text/html; charset=utf-8')
print()  # 空行，告诉服务器结束头部
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
try:
    query = parse_qs(input())
    for filename in query['filename']:
        basename = os.path.basename(filename)
        if os.path.exists(upload_dir + basename):
            os.remove(upload_dir + basename)
            deleted.append(basename)
        else:
            non_existent.append(basename)
except:
    pass
print('<form method="post">')
print('<table border="1"><thead><tr><td></td><td><b>文件名</b></td></tr></thead><tbody>')
file_list = os.listdir('upload')
for name in file_list:
    print(f'<tr><td><input type="checkbox" name="filename" value="{name}"></td>'
          f'<td><a href="../upload/{name}">{name}</a></td></tr>')
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
