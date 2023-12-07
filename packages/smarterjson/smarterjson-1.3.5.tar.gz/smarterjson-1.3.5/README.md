# <font color=gree>Smarterjson智能json</font>

a python package, **smarter than python's json**\
一个python包，**比python的json更加智能**

## code show: lib basic module skills</br>代码演示：模块基础功能

```python basic module skills
import smarterjson

smarterjson.write({"python": "hello"}, fp="smarterjson.json")
smarterjson.read(("python",), fp="smarterjson.json", return_type=str)
smarterjson.append({"C++": "world"}, fp="smarterjson.json")
smarterjson.exist("C++", fp="smarterjson.json")
smarterjson.revise(("C++",), "good", fp="smarterjson.json")

smarterjson.key_parent("hello", fp="smarterjson.json")
smarterjson.value_parent("good", fp="smarterjson.json")
```

## code show: lib view module skills</br>代码演示：view预览模块功能

This modules is used to summon parent tree\
这个模块是用来生成父级树
```python view modules skills
import smarterjson.view as view

view.tree("values  ->  key1  ->  value")
```