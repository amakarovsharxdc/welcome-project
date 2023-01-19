from typing import Dict, List, Tuple, Any, Union
from collections import ChainMap


class EmptyNodes(Exception):
    pass

class EmptyNode(Exception):
    pass

class NonValidNestedStruct(Exception):
    pass

class NonValidRootKey(Exception):
    pass

class DataValidator:

    @classmethod
    def check_for_param(cls, arg:str)->bool:
            """
            check_for_param 

            проверка является ли строка параметром

            Args:
                arg (str): входная строка

            Returns:
                bool: True - является/False - не является
            """
            if not '{' in arg and not '}' in arg:
                return False
            else:
                return True

            
  

class DataConstructor:
     
    
    def __init__(self, output:Dict|None = None):
        self.output = output if output else {}

    def set_output_root_key(self, arg:str)->None:
        # проверка на наличие ключей 
        if not self.output.keys():
            self.output.update({arg:{}})
        else:
            if not arg in self.output.keys():
                raise NonValidRootKey
            
    def set_nested_child(self, arg:List[str])->Dict[str, Any]|str:
        """
        set_nested_child 

        создание вложенного словаря

        Args:
            arg (List[str]): массив аргументов

        Returns:
            
        """
        if len(arg) > 1:
            return {arg[0] : self.set_nested_child(arg[1:])}
        return arg[0]

    def get_last_nested_child(self, arg:dict)->List[Dict[str, str]]:
        """
        get_last_nested_child 

        получение словаря из последнего узла
        
        Args:
            arg (dict): словарь со вложенной структурой

        Returns:
            List[Dict[str, str]] массив всех узлов
        """
        output = [nested for v in arg.values() if isinstance(v, dict) for nested in self.get_last_nested_child(v)]
        if not output:
            output = [arg]
        return output

    def set_nested_child_data(self, source:dict, arg:Any):
        """
        set_nested_child_data

        изменение значения для ключа во вложенном словаре

        Args:
            source (dict): исходные данные
            arg (Any): входное значение
        """
        key = next(k for k in source.keys())
        value = next(v for v in source.values())
        source[key] = {value:arg}

    def set_node_data(self, arg:Tuple[str, str])->Dict[str, Any]:
        node = None
        method, path = arg
        # разбор строки на элементы
        _, _, _,root, *nodes  = path.split("/")
        if not nodes:
            raise EmptyNodes
        # установка ключа верхнего уровня
        self.set_output_root_key(root)
        # получение всех элементов отвечающих требованию
        not_param_nodes = [elem for elem in nodes if not DataValidator.check_for_param(elem)]
        if not not_param_nodes:
            raise EmptyNode  
        if len(not_param_nodes)==1:
            node =  {not_param_nodes[0]:method}
        elif len(not_param_nodes) >1:
            nested_struct = self.set_nested_child(not_param_nodes)
            if not isinstance(nested_struct, dict):
                raise NonValidNestedStruct
            last_nested = self.get_last_nested_child(nested_struct)[-1] 
            self.set_nested_child_data(last_nested, method)
            node = nested_struct 
        if not node:  
            raise EmptyNode
        return node           
       
    def construct(self, args:List[Tuple[str, str]]):
        new_nodes = []
        # наполнение массива значениями узлов
        for arg in args:
            new_nodes.append(self.set_node_data(arg))
        # проверка на наличие полученных узлов
        if not new_nodes:
            raise EmptyNodes
        # получение ключа 
        output_key = [k for k in self.output.keys()][-1]
        # объединения массива словарей в единый словарь
        # получение массива текущих узлов
        output_nodes = [v for v in self.output.values() if v]
        # добавление к текущим узлам
        output_nodes.extend(new_nodes)
        # создание структуры словарей из массива словарей
        output_validated_subs = dict(ChainMap(*output_nodes))
        # обновление значений в исходном словаре
        self.output[output_key] = output_validated_subs
        return self.output


constructor1 = DataConstructor()
inc1 = [("GET", "/api/v1/cluster/metrics"),
              ("POST", "/api/v1/cluster/{cluster}/plugins"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]

output1 = constructor1.construct(inc1)


constructor2 = DataConstructor(output1)
inc2 = [("GET", "/api/v1/cluster/freenodes/list"),
              ("GET", "/api/v1/cluster/nodes"),
              ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
              ("POST", "/api/v1/cluster/{cluster}/plugins")]

output2 = constructor2.construct(inc2)

print(output2)

