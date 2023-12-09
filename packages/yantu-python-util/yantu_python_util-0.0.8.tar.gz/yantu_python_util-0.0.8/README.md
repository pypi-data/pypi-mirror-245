

## 主要功能
1. 基本文件操作
   - `json`文件读写 

>  load_json 读取json文件  
>  write_json 写入json文件


## 使用方法
```
pip install yantu_python_util
```

```python
from yantu_python_util.operate_json import write_json, load_json

write_json(data="your json data", filepath="your file path")
load_json(filepath="your file path")
```


## 上传方法
1. 构建源文件

``` python
python setup.py sdist bdist_wheel build
```
3. 上传源文件
```shell
twine upload dist/*
```
