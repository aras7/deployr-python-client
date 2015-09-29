Deployr python client
=======

First version of a simple python client for deployr.

Usage:
------

* Create instance and configure
```python
from deployr_connection import DeployRConnection

host = "http://your.host.com:port/deployr/"
deployr_connection = DeployRConnection(host)
```

* Login

```python
deployr_connection.login("username", "Passw0rd")
```

* Create project

```python
data = {"projectname": "some name", "projectdescr": "some description"}
status_response, response = deployr_connection.call_api("r/project/create/", data)
```

* Execute script

```python
data = {"project": "your project identifier", "filename": "source.R", "directory": "home", "author": "your_author"}

status_response, response = deployr_connection.call_api("r/project/execute/script/", data)
```

* Upload files to project working directory

```python
data = {"project": "your project identifier", "filenam": "your_file_name.ext", "descr": "your file description", "overwrite": True}
files = {"file": file_content} #  file content could be 'open("/url/file.ext", 'rb').read()'

status_response, response = deployr_connection.call_api("r/project/directory/upload/", data, files=files)
```

* Add rinputs

```python
deployr_connection.set_rinput("variable", "primitive", 123456)
```

* Add routputs

```python
deployr_connection.set_routput("variable")
```

[Check this for more api details](http://deployr.revolutionanalytics.com/documents/dev/api-doc/guide/single.html)
