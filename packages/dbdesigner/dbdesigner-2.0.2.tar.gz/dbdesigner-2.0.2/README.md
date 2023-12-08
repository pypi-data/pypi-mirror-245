# DBDesigner

```
python setup.py sdist
twine upload dist/*

```

* 创建用户验证文件 ~/.pypirc
```
[distutils]
index-servers=pypi
 
[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <password>
```