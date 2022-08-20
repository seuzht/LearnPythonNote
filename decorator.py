'''
@description:usages of decorator
@author:Denn Zhang
@date:2022/08/18
'''
#!/usr/bin/env python
import functools

#python的编译期和运行期
#装饰器在运行期确定所装饰的对象，而继承是编译期就确定子类化对象
#python解释器包含两个部分：编译器（编译期将py文件代码编译成字节码.pyc）+ 虚拟机（运行期逐行字节码）
#https://zhuanlan.zhihu.com/p/162720316
#https://www.jianshu.com/p/2d59930c6efc


#装饰器就是一个语法糖，其本质是利用特殊的函数(返回是一个函数回调)/类(__call__或者描述符)在运行期扩展原来被装饰的函数的功能，而不需要修改原函数的代码

#装饰器分类：
###1.装饰器本身的类型是函数还是类
###2.装饰器所修饰的对象是函数还是类

''' 类型1:
------------------------------------------------------
函数型装饰器修饰函数
------------------------------------------------------
'''
#无参数的装饰器函数-------装饰(扩展)一个函数
def decoratorFnWithoutParas(fn):
    print('无参函数装饰器------before fn 调用')
    @functools.wraps(fn)  #保存内省
    def wrapper(*args,**kwargs):
        print('without---wrapper---回调执行')
        print("[DEBUG]: enter {}()".format(fn.__name__))
        fn(*args,**kwargs) #被修饰函数回调，是一种闭包
    return wrapper #返回装饰后的函数对象供使用


#带参数的装饰器函数-------装饰(扩展)一个函数
def decoratorFnWithParas(level):
    print('with---装饰器定义')
    def decorator(fn):
        print('with---fn-----装饰器调用')
        #@functools.wraps(fn)
        def wrapper(*args,**kwargs):
            print('with---fn---wrapper----回调执行')
            print("[{0}]: logging  {1}()".format(level, fn.__name__))
            fn(*args,**kwargs) #被修饰函数回调，是一种闭包
        return wrapper
    return decorator


#带参数的装饰器函数-------装饰(扩展)一个函数
def decoratorFnWithParas2(level):
    print('with2---装饰器定义')
    def decorator(fn):
        print('with2---fn-----装饰器调用')
        #@functools.wraps(fn)
        def wrapper(*args,**kwargs):
            print('with2---fn---wrapper----回调执行')
            print("[{0}]: 2 logging  {1}()".format(level, fn.__name__))
            fn(*args,**kwargs) #被修饰函数回调，是一种闭包
        return wrapper
    return decorator

''' 类型2:
------------------------------------------------------
类装饰器修饰函数
带参数和不带参数指的是类实例化时带不带参数
------------------------------------------------------
'''
#无参类装饰器
class DecoratorClassWithoutParas(object):
    def __init__(self,fn): #无参数类装饰器在类初始化时传入所修饰的函数对象
        print('无参类装饰器---init调用.....')
        self.fn = fn
    def __call__(self,*args,**kwargs):#魔法方法__call__实现所修饰函数的调用
        print('无参类装饰器---—__call__执行.....')
        return self.fn(*args,**kwargs)
#带参类装饰器
class DecoratorClassWithParas(object):
    def __init__(self,val): #带参类装饰器，参数val
        self.val = val
    def __call__(self,fn):
        def wrapper(*args,**kwargs):
            return fn(*args,**kwargs)
        return wrapper

#类中的函数作为装饰器,本质上还是函数型装饰器
class DecoratorFnInClass(object):
    def __init__(self):
        pass
    def decorator(fn):#也可以是带self的成员函数，则需要用实例对象的函数去装饰其他函数
        def wrapper(*args,**kwargs):
            print('decorator fn in Class-----执行')
            fn(*args,**kwargs)
        return wrapper
    
''' 类型3:
------------------------------------------------------
函数装饰器/非数据描述符  修饰 类
返回值是一个类而不是函数; 作用: 运行时通过cls修改类的属性和方法;
用于修饰类的函数装饰器可以带参或者不带参，原理同上;
------------------------------------------------------
'''
#无参/带参函数装饰器通过cls在运行时修改被装饰类的属性和方法
def decoratorfnforclass(fn):#带参数装饰器
    def wrapper(cls): #需要一个cls参数用于接受被修饰类
        cls.__repr__ = lambda self:super(cls,self).__repr__()[:8]
        cls.addProperty = 'newClassProperty' #运行时为被修饰类添加了一个属性
        cls.addFn = fn  #运行时为被修饰类添加了一个方法
        return cls
def additionalFn(str):
    print(str)

#如果函数装饰器在内部弃用cls并新定义类，来重写被装饰类，这种写法没有实际意义;
#如果函数装饰器内部通过cls创建子类，即对cls使用闭包则无法保存内省;这个是需要避免的情况;
def decoratorfnforclasswithnewclass(cls):
    #deprecate cls and define a new class
    class NewClass(object):
        pass
    #or create a subclass from cls
    class SubClassFromCls(cls):
        #无法保持内省，生成的对象不再是被修饰类的实例，而是这里新创建的类的实例
        #这会影响__name__和__doc__属性的使用
        pass
    return NewClass


#应用
decoratorFnInClass = DecoratorFnInClass()
#多个装饰器执行顺序：
###1.装饰器定义准备从上到下（传入fn前）
###2.装饰器调用（传入fn后)从下到上
###3.装饰器回调函数执行（wrapper 传入*args和**kwargs后)从上到下
@DecoratorFnInClass.decorator #类中定义的函数(成员函数/类函数)也可以作为函数型装饰器，只要符合函数型装饰器定义规则
@DecoratorClassWithoutParas
@decoratorFnWithParas2(level='WARNING')
@decoratorFnWithParas(level='INFO')  
@decoratorFnWithoutParas
def ordFunc(iNum,outStr):
    print("被修饰函数本地执行:iNum: {}  outStr: {}".format(iNum,outStr))


@decoratorfnforclass(additionalFn)
class OrdClass(object):
    pass
    



if __name__ == '__main__':
    ordFunc(0,"HELLO DECORATOR")