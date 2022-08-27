'''
@description: Python/C API extension
@author: Dennis Zhang
@date:2022/08/25
'''
#!/usr/bin/env python3

#python的扩展有3种方式:
#1.无扩展的动态库接口(√)
    ## 通过ctypes模块或CFFI库调用C库;不需要修改c库的任何代码,只需利用ctypes模块做好数据类型转换;
    ## 1.1 ctypes标准库模块
        ###1.1.1 python代码中加载c/c++动态或共享库
        ###1.1.2 使用ctypes模块提供的相应类进行包装,使ctypes调用c函数时能传递正确的数据类型
        ###1.1.3 传递python函数作为C的回调
        ###1.1.4 调用c函数
import ctypes
from ctypes.util import find_library
import numbers
from random import shuffle
#libc = ctypes.cdll.LoadLibrary("xxx.so")
libc = ctypes.cdll.LoadLibrary(find_library('c'))

#----------------如果需要为C提供回调----------
#ctypes模块的一个工厂函数CFUNCTYPE()
#作为python函数的包装器,可以把python函数包装成C的函数回调
CMPFUNC = ctypes.CFUNCTYPE(
    #返回类型 int
    ctypes.c_int,
    #第一个参数类型 int*
    ctypes.POINTER(ctypes.c_int),
    #第二个参数类型 int*
    ctypes.POINTER(ctypes.c_int)
)
#python函数:比较函数
def ctypes_int_compare(a,b):
    print(" %s cmp %s " %(a[0],b[0]))
    return a[0] - b[0]
#------------------------------------------
def main():
    numbers = list(range(5))
    shuffle(numbers)
    print("shuffled: ",numbers)
    #利用ctypes基础类型创建C接口能识别的新类型
    NumbersArray = ctypes.c_int * len(numbers)
    c_array = NumbersArray(*numbers) #初始化NumbersArray数组
    libc.qsort(
        c_array,
        len(c_array),
        ctypes.sizeof(ctypes.c_int),
        CMPFUNC(ctypes_int_compare) #python函数被包装后作为C的回调
    )
    print("sorted: ",list(c_array))

if __name__ == "__main__":
    main()
    ## 1.2 CFFI包
        ### cffi更强调重用纯C代码，而不是在单个模块中提供大量的Python API.
        ### 它允许使用c编译期将集成层的某些部分代码自动编译为扩展,因此它可以用作填补C扩展和ctypes之间差距的混合解决方案;
from random import shuffle
from cffi import FFI
ffi = FFI()
#---------------------cffi的回调包装处理---------
ffi.cdef('''
void qsort(void *base,size_t nel,size_t width,
int (*compare)(const void*,const void*));
''')
C = ffi.dlopen(None)

@ffi.callback("int(void*,void*)")
def cffi_int_compare(a,b):
    #回调签名需要类型的精确匹配
    #这涉及到比ctypes更少的魔法
    #但需要更详细更明确的类型转换
    int_a = ffi.cast('int*',a)[0]
    int_b = ffi.cast('int*',b)[0]
    return int_a - int_b
#------------------------------------------------
def main():
    numbers = list(range(5))
    shuffle(numbers)
    c_array = ffi.new('int[]',numbers)
    C.qsort(
        c_array,
        len(c_array),
        ffi.sizeof('int'),
        cffi_int_compare
    )
##################################################################################################

##################################################################################################
#2.改造c代码,通过对C代码接口加上python wrapper,使得其可以在python环境中被调用;
    ## Python.h + Python/C API + C/C++ + 打包 => Python C扩展模块
    ## 2.1 三步
        ###2.1.1 定义cfunc_py接口作为源cfunc接口的wrapper,包含几个主要类型、宏和Python/C API:
            ####数据类型:PyObject 
            ####Apis:PyArg_ParseTuple;Py_BuildValue;PyErr_SetString();PyLong_FromLong
            ####释放GIL宏:Py_BEGIN_ALLOW_THREADS   Py_END_ALLOW_THREADS
            ####引用计数:Py_INCREF  py_DECREF (自己维护引用计数难度较大,容易出错)
        ###2.1.2 定义扩展函数定义结构体数组PyMethodDef[]
        ###2.1.3 定义整个扩展模块的结构体struct PyModuleDef
        ###2.1.4 扩展模块的初始化函数PYMODINIT_FUNC PyInit_func(void){Py_Initialize(); return PyModule_Create(&PyModuleDef)}
        ###2.1.5 setuptools构建 
    ## ref https://zhuanlan.zhihu.com/p/164598060
    ## ./extension.c
#3.利用cython:
    ## cython的C扩展主要是一个自动过程，它不需要你写一个.C文件，而是使用一种Cython特殊的后缀为.pyx扩展文件,
    ## 经过cython库编译器处理后生成python库文件,Win下后缀为.pyd,Linux下为动态链接库.so,然后就可以在python里import了;
    ## ref https://zhuanlan.zhihu.com/p/49498032
    ## 3.1 cython作为源码编译器
        ### 使用纯python代码创建扩展,不用修改源C代码,实现源到源编译;
        ### 并用cythonize函数将.py文件编译成c代码;本质上cython使用Python/C API执行了源到源的编译
    ## 3.2 cython作为语言,。pyx文件
        ### cdef 关键字声明接受和返回C类型的C风格函数 
        ### with nogil
        ### ref ./fibonacci.pyx文件

from tkinter import N
from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'fibonacci',
    ext_modules=cythonize(['fibonacci.py'])
)