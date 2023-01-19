from typing import Dict, List, Tuple, Any, Union
from collections import ChainMap


class EmptyChildValue(Exception):
    pass


class NonValidRootValue(Exception):
    pass

class NonValidArray(Exception):
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
        self.subs:List[Dict[str,str|Dict[str, Any]]] = []

    def _set_output_root_key(self, arg:str)->None:
        # проверка на наичие ключей 
        if not self.output.keys():
            self.output.update({arg:{}})
        else:
            if not arg in self.output.keys():
                raise NonValidRootValue
            
    def _set_nested_child(self, arg:List[str]):
        """
        _set_nested_child 

        создание вложенного словаря

        Args:
            arg (List[str]): массив аргументов

        Returns:
            
        """
        if len(arg) > 1:
            return {arg[0] : self._set_nested_child(arg[1:])}
        return arg[0]

    def _get_last_nested_child(self, arg:dict)->List[Dict[str, str]]:
        """
        _get_last_nested_child _summary_

        получение словаря из последнего узла
        
        Args:
            arg (dict): словарь со вложенной структурой

        Returns:
            List[Dict[str, str]] массив всех узлов
        """
        output = [nested for v in arg.values() if isinstance(v, dict) for nested in self._get_last_nested_child(v)]
        if not output:
            output = [arg]
        return output

    def _set_nested_child_data(self, source:dict, arg:Any):
        """
        _set_nested_child_data _summary_

        изменение значения для ключа во вложенном словаре

        Args:
            source (dict): исходные данные
            arg (Any): входное значение
        """
        key = next(k for k in source.keys())
        value = next(v for v in source.values())
        source[key] = {value:arg}

    def _set_data(self, arg:Tuple[str, str])->None:
       
        method, path = arg
        # разбор строки на элементы
        _, _, _,root, *nodes  = path.split("/")
        # сверка ключа верхнего уровня
        self._set_output_root_key(root)
        not_param_nodes = [elem for elem in nodes if not DataValidator.check_for_param(elem)]
        if not not_param_nodes:
            raise ValueError
        if len(not_param_nodes)==1:
            self.subs.append({not_param_nodes[0]:method})
        if len(not_param_nodes) >1:
            nested_struct = self._set_nested_child(not_param_nodes)
            last_nested = self._get_last_nested_child(nested_struct)[-1] #type: ignore
            self._set_nested_child_data(last_nested, method)
            self.subs.append(nested_struct) #type: ignore                      
       
    def construct(self, args:List[Tuple[str, str]]):
        for arg in args:
            self._set_data(arg)
        # получение ключа 
        output_key = [k for k in self.output.keys()][-1]
        # объединения массива словарей в единый словарь
        output_current_subs = [v for v in self.output.values() if v]
        output_current_subs.extend(self.subs)
        output_validated_subs = dict(ChainMap(*output_current_subs))
        self.output[output_key] = output_validated_subs
        return self.output


# constructor1 = DataConstructor()
# inc1 = [("GET", "/api/v1/cluster/metrics"),
#               ("POST", "/api/v1/cluster/{cluster}/plugins"),
#               ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]

# output1 = constructor1.construct(inc1)


# constructor2 = DataConstructor(output1)
# inc2 = [("GET", "/api/v1/cluster/freenodes/list"),
#               ("GET", "/api/v1/cluster/nodes"),
#               ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
#               ("POST", "/api/v1/cluster/{cluster}/plugins")]

# output2 = constructor2.construct(inc2)

# print(output2)

