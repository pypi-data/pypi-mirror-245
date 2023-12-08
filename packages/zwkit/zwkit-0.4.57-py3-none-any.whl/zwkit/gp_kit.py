# gplearn_kit
import numpy as np
from joblib import wrap_non_picklable_objects
import torch
def is_float_num(str):
    try:
        float_value = float(str)
        return True
    except ValueError:
        return False





class _Function(object):

    def __init__(self, function, name, arity, ts=False, ts_group=None):
        self.function = function
        self.name = name
        self.arity = arity
        self.index = None
        if ts is True:
            self.ts_arity = arity - 1
        else:
            self.ts_arity = arity
        self.ts = ts
        self.days = ts_group

    def __call__(self, *args):
        return self.function(*args)


def make_function(*, function, name, arity, wrap=True, ts=False, ts_group=None):

    if not isinstance(arity, int):
        raise ValueError('arity must be an int, got %s' % type(arity))
    if not isinstance(function, np.ufunc):
        if function.__code__.co_argcount != arity:
            raise ValueError('arity %d does not match required number of '
                             'function arguments of %d.'
                             % (arity, function.__code__.co_argcount))
    if not isinstance(name, str):
        raise ValueError('name must be a string, got %s' % type(name))
    if not isinstance(wrap, bool):
        raise ValueError('wrap must be an bool, got %s' % type(wrap))

    if wrap & ts is False:
        return _Function(function=wrap_non_picklable_objects(function),
                         name=name,
                         arity=arity)
    if ts is True:
        return _Function(function=function,
                         name=name,
                         arity=arity,
                         ts=ts,
                         ts_group=ts_group)
    return _Function(function=function,
                     name=name,
                     arity=arity)


def formula_build(name_function, process_function, columns, structure):
    """
    公式实例化
    :param name_function: 函数名称
    :param process_function: 函数实例
    :param columns: 列名称
    :param structure: 公式结构
    :return:
    """
    # print("formula_build name_function:", name_function)
    # print("formula_build process_function:", process_function)
    # print("formula_build columns:", columns)
    # print("formula_build structure:", structure)

    result = list()
    structure_list = structure.copy()
    for i in range(len(structure_list)):
        # 是否包含.0
        if structure_list[i].find('.000') != -1:
            result.append(float(structure_list[i]))
        elif structure_list[i] in columns:
            result.append(structure_list[i])
        elif is_float_num(structure_list[i]):
            result.append(float(structure_list[i]))
        else:
            result.append(process_function[name_function.index(structure_list[i])])
    return result


def factor_calculate(data, program):
    """
        因子计算
        :param program: 公式
        :param data: 数据源
        :return:
        """
    # Check for single-node programs
    node = program[0]
    if isinstance(node, float) | isinstance(node, int):
        return np.repeat(node, data.shape[0])

    apply_stack = []

    for node in program:

        if isinstance(node, _Function):
            apply_stack.append([node])
        else:
            # Lazily evaluate later
            apply_stack[-1].append(node)

        while len(apply_stack[-1]) == apply_stack[-1][0].arity + 1:
            # Apply functions that have sufficient arguments
            function = apply_stack[-1][0]
            terminals = [np.repeat(t, data.shape[0]) if (isinstance(t, float) | isinstance(t, int))
                         else data[t] if isinstance(t, str)
            else t for t in apply_stack[-1][1:]]
            intermediate_result = function(*terminals)
            if len(apply_stack) != 1:
                apply_stack.pop()
                apply_stack[-1].append(intermediate_result)
            else:
                return intermediate_result
def factor_calculate_cuda(data, program):
    """
        因子计算
        :param program: 公式
        :param data: 数据源
        :return:
        """
    # Check for single-node programs
    node = program[0]
    if isinstance(node, float) | isinstance(node, int):
        return np.repeat(node, data.shape[0])

    apply_stack = []

    for node in program:

        if isinstance(node, _Function):
            apply_stack.append([node])
        else:
            # Lazily evaluate later
            apply_stack[-1].append(node)

        while len(apply_stack[-1]) == apply_stack[-1][0].arity + 1:
            # Apply functions that have sufficient arguments
            function = apply_stack[-1][0]
            terminals = [np.repeat(t, data.shape[0]) if (isinstance(t, float) | isinstance(t, int))
                         else torch.tensor(data[t],dtype=torch.float32).cuda() if isinstance(t, str)
            else t for t in apply_stack[-1][1:]]
            intermediate_result = function(*terminals)
            if len(apply_stack) != 1:
                apply_stack.pop()
                apply_stack[-1].append(intermediate_result)
            else:
                return intermediate_result
