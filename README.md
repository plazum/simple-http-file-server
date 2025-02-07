# simple-http-file-server

一个极简的HTTP文件服务器，可以上传、下载和删除文件。

A truly minimal HTTP file server that supports file upload, download, and deletion.

无需任何第三方库，只需在仓库根目录下执行如下命令即可运行：

No need for any third-party libraries. Just run the following command in the root directory of the repository to start the server:

```bash
python -m http.server --cgi
```

## 使用说明

如果在Linux下运行的时候遇到`Error code: 403 Message: CGI script is not executable`，可能是脚本文件没有执行权限，请在仓库根目录下执行如下命令：

```bash
chmod g+x cgi-bin/*.py
```

## 代码说明

- `index.html`：首页，可以上传文件。
- `cgi-bin/upload.py`：处理文件上传逻辑。
- `cgi-bin/file-manager.py`：展示已上传的文件（upload目录下的文件），可以用浏览器访问和下载文件，可以删除指定的文件。
