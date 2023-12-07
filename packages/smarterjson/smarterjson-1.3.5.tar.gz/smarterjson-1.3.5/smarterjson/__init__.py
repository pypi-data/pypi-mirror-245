import json

__version__ = __VERSION__ = '1.3.5'
__all__ = ['write', 'append', 'revise', 'read', 'exist', 'value_parent', 'key_parent',
           'list_key', 'list_value', 'list_line', 'list_split']

def write(__value__: dict,fp: str, encoding: str="utf-8", ensure_ascii: bool=False, back: bool=True,indent: int=3):
    """
    Write data into json file,
    :param __value__: You'll write data into file
    :param fp: File path
    :param encoding: encode, such as UTF-8, GB18030, GBK *utf-8
    :param ensure_ascii: decode unicode *False
    :param indent: indent *3
    :param back: return or do not return write before data, *True
    :return: if back equals True, then return write before data. Else None *True
    """
    ori_data = None
    with open(fp, "r", encoding=encoding) as f:
        try:
            ori_data = data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    data = [__value__]
    with open(fp, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
        f.close()
    if back:
        return json.dumps(ori_data, ensure_ascii=False, indent=indent)

def append(__value__: dict,fp: str, encoding: str="utf-8", ensure_ascii: bool=False, indent: int=3):
    """
    Append data into json file
    :param __value__: You'll append data into file
    :param fp: File path
    :param encoding: encode, such as UTF-8, GB18030, GBK *utf-8
    :param ensure_ascii: decode unicode *False
    :param indent: indent *3
    :return: None
    """
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    state = True
    try:
        ori = []
        now = ''
        values = ''

        for key, value in __value__.items():
            now = key
            values = value
        for i in range(len(data)):
            for key, value in data[i].items():
                ori.append(key)
        if now in ori:
            data[ori.index(now)][now] = values
            state = False

    except:
        pass

    finally:
        if state:
            data.append(__value__)
    with open(fp, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
        f.close()

def read(__content__: tuple, fp=None, encoding: str="utf-8",return_type: type=str):
    """
    Smart read the json file,
    test.json:
    [
        {"a": {
                "b": "a"
            }
        }
    ]
    main.py:
    from smarterjson import read

    read(__content__=("a","b"), fp="test.json")


    :param __content__: You want to search the value's content, for example, If data=[{"a": {"b": "c"}}],
                        then __content__=('a', 'b')
    :param fp: File path
    :param encoding: encoding, such as UTF-8, GB18030, GBK *utf-8
    :param return_type: after read the file, return data's type *str
                        Python's type
                        str -> return str(data) | str
                        list -> return [data] | list
                        dict -> return {json.dumps(data)} | dict
                        int -> return len(data) | length

                        Basic's type:
                        list_split -> return list(str(data)) / ['a','b','c']
                        list_line -> ['"t": "abc"', '"t2"': "cba"]
                        list_key -> ["t", "t1"]
                        list_value -> ["abc", "cba"]
    :return: any or basic
    """
    s_type = [list, str, int, dict, list_split, list_line, list_key, list_value]
    if return_type not in s_type:
        raise ReturnTypeError(f"Invalid return type: '{return_type}', only support {s_type}")
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    ori = []
    for i in range(len(data)):
        for key, value in data[i].items():
            ori.append(key)
    try:
        if isinstance(__content__, tuple):
            result = data[ori.index(__content__[0])]
            for item in __content__:
                result = result[item]
            if return_type == str:
                return str(result)
            elif return_type == list:
                return [result]
            elif return_type == dict:
                return json.dumps(result)
            elif return_type == int:
                return len(result)
            elif return_type == list_split:
                return list(str(result))
            elif return_type == list_line:
                return json.dumps(result, indent=3).replace(" ", "").replace(",", "").split("\n")[1:-1]
            elif return_type == list_key:
                return list(result)
            elif return_type == list_value:
                return list(result.values())
        else:
            raise ValueError("Invalid content type, should be a tuple")
    except (KeyError, TypeError):
        raise NotFoundOptionsError(f"Not found '{__content__}', please check content or cannot change the type to {return_type}")
    except IndexError:
        raise EmptyFileError(f"This file {fp} is empty, please write '[]' data")

def exist(__key__: str, fp=None, encoding: str="utf-8") -> bool:
    """
    Search the key in json file,
    test.json:
    [
        {"a": {
                "b": "a"
            }
        }
    ]
    main.py:
    from smarterjson import exist

    print(exist(__find__="a", fp="test.json")) # True
    print(exist(__find__="d", fp="test.json")) # False

    :param __key__: You'll find data
    :param fp: File path *None
    :param encoding: encoding, such as UTF-8, GB18030, GBK *utf-8
    :return: bool, if __find__ in json data head return True, else return False
    """
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    ori = []
    for i in range(len(data)):
        for key, value in data[i].items():
            ori.append(key)
    if __key__ in ori:
        return True
    else:
        return False

def revise(__content__: tuple, __value__: any, fp=None, encoding: str="utf-8", ensure_ascii=False, indent: int=3):
    """
    Revise the json file,
    before test.json:
    [
        {"a": {
                "b": "a"
            }
        }
    ]
    main.py:
    from smarterjson import revise

    revise(__content__=("a',"b"),__value__="111", fp="test.json")

    after test.json:
    [
        {"a": {
                "b": "111"
            }
        }
    ]

    :param __content__: json file content
    :param __value__: You want to revise value
    :param fp: File path
    :param encoding: encoding such as UTF-8
    :param ensure_ascii: ensure_ascii
    :param indent: indent
    :return: None
    """
    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if type(data) != list:
        data = [data]
    ori = []
    for i in range(len(data)):
        for key, value in data[i].items():
            ori.append(key)
    if isinstance(__content__, tuple):
        for item in __content__:
            data[ori.index(__content__[0])][item] = __value__
    with open(fp, "w", encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)

def value_parent(__value__, fp: str=None, encoding: str="utf-8", return_type: type=str):
    """
    Find json data's values' parents,
    values  ->  key1  --> key2 --> ... --> __value__
    :param __value__: You want to find the value in data
    :param fp: file path
    :param encoding: encoding, such as UTF-8, GB18030, GBK *utf-8
    :param return_type: return type, support str or list *str
    :return: result or None
    """
    types = [str, list]
    if return_type not in types:
        raise ReturnTypeError(f"Unsupport types, only support {types}")
    def father(json_data, value, path=""):
        if isinstance(json_data, dict):
            for key, val in json_data.items():
                if val == value:
                    return f"values{path}  ->  {key}  ->  {val}"
                elif isinstance(val, dict) or isinstance(val, list):
                    result = father(val, value, f"{path}  ->  {key}")
                    if result:
                        return result
        elif isinstance(json_data, list):
            for item in json_data:
                result = father(item, value, path)
                if result:
                    return result
        return None

    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if return_type == str:
        return father(data, __value__)
    else:
        return father(data, __value__).replace(" ", "").split("->")

def key_parent(__key__, fp: str=None, encoding: str="utf-8", return_type: type=str):
    """
    Find json data's keys' parents,
    keys  ->  key1  --> key2 --> ... --> __key__
    :param __key__: You want to find the key in data
    :param fp: file path
    :param encoding: encoding, such as UTF-8, GB18030, GBK *utf-8
    :param return_type: return type, support str or list *str
    :return: result or None
    """
    types = [str, list]
    if return_type not in types:
        raise ReturnTypeError(f"Unsupport types, only support {types}")
    def father(json_data, key, path=''):
        if isinstance(json_data, dict):
            for k, val in json_data.items():
                if k == key:
                    return f"keys{path}  ->  {key}"
                elif isinstance(val, dict) or isinstance(val, list):
                    result = father(val, key, f"{path}  ->  {k}")
                    if result:
                        return result
        elif isinstance(json_data, list):
            for item in json_data:
                result = father(item, key, path)
                if result:
                    return result
        return None

    with open(fp, "r", encoding=encoding) as f:
        try:
            data = json.load(f)
        except:
            data = []
        f.close()
    if return_type == str:
        return father(data, __key__)
    else:
        return father(data, __key__).replace(" ","").split("->")


# show error
class ReturnTypeError(TypeError):
    pass
class NotFoundOptionsError(ValueError):
    pass
class EmptyFileError(IndexError):
    pass

# type
class list_split(list):
    pass
class list_line(list):
    pass
class list_key(list):
    pass
class list_value(list):
    pass
