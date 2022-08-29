'''
@description:  with 语句-------上下文管理器
@author:Denn Zhang
@date:2022/08/22
'''

#!/usr/bin/env python
'''语法： 
    with context_expression [as target(s)]:
        with-body
'''
# ref https://zhuanlan.zhihu.com/p/317360115

#with 后面的的对象context_expression需要实现「上下文管理器协议」; as后面的target是上下文管理器__enter__方法的返回值;
#1.自定义类+实现上下文管理器协议
    ##一个类在 Python 中，只要实现以下方法，就实现了「上下文管理器协议」：
        ### __enter__：在进入 with 语法块之前调用，返回值会赋值给 with 的 target
        ### __exit__：在退出 with 语法块时调用,如果在 with 语句块内发生了异常,那么 __exit__ 方法可以拿到关于异常的详细信息:
            #### exc_type：异常类型
            #### exc_value：异常对象
            #### exc_tb：异常堆栈信息
#执行顺序是: 上下文管理器中的__enter__ (返回值作为target)  => with-body体执行  => __exit__
class ContextManager(object):
    def __enter__(self):
        #do sth
        target = 1 
        print('__enter__ is called')
        #raise TypeError('there is a typeError here')#__enter__中的异常需要自行处理,不会被__exit__捕获
        return target
    def __exit__(self, exc_type, exc_value, exc_tb):
        #可以针对异常做特殊处理
        print('exc_type: %s' % exc_type)
        print('exc_value: %s' % exc_value)
        print('exc_tb: %s' % exc_tb)
''''
class File:
    def __enter__(self):
        #返回操作对象
        return file_obj 
    def __exit__(self, exc_type, exc_value, exc_tb):
        # with 退出时释放文件资源
        file_obj.close()
        # 如果 with 内有异常发生 抛出异常
        if exc_type is not None:
            raise exception
'''
with ContextManager() as t:
    #do sth, if exception occurs here, __exit__ will capture it and executed.
    print('target is %s' %t)

#2.1.contextlib模块: contextmanager装饰器
#当使用contextmanager 装饰器后，就不用再写一个类来实现上下文管理协议，只需要用contextmanager装饰含yield的生成器方法，就可以实现相同的功能;
#注意：在使用 contextmanager 装饰器时，如果被装饰的方法内发生了异常，那么我们需要在自己的方法中进行异常处理，否则将不会执行 yield 之后的逻辑
from contextlib import  contextmanager
#装饰器+一个方法就可以构成一个上下文管理器，不需要自己定义一个类再去实现上下文管理协议
@contextmanager
def ContextManagerFnWithDecorator(): #含yield关键字的生成器函数
    print('before')
    try:
        yield 'hello' #返回值传给t
        # 这里发生异常 必须自己处理异常逻辑 否则不会向下执行
        # a = 1 / 0 
    finally:
        print('after') #在with语句块执行后再回到这里执行
#执行顺序：before =>  (t = ''hello) with语句 =>  after
with ContextManagerFnWithDecorator() as t:
    print('t is %s' %t)


#2.2.contextlib标准库中closing方法模块的使用
#所修饰的资源对象类必须实现close方法才能使用closing
#closing 主要用在已经实现 close 方法的资源对象上
class ResourceClassWithClose(object):
    def open(self):
        return self
    # 定义了 close 方法才可以使用 closing 装饰器
    def close(self):
        print('closed')

from contextlib import closing
with closing(ResourceClassWithClose().open()) as f:  
    #with语句块执行结束后自动执行ContextManagerClassWithDecorator类的close方法
    print('do something')
'''等同于 
f = ResourceClassWithClose().open() try:
    #do sth
finally:
    f.close()
''' 

#3.应用:-----------------------------------------------------------------
#3.1 Redis分布式锁
from contextlib import contextmanager
import redis
@contextmanager
def lock(redis, lock_key, expire):
    try:
        locked = redis.set(lock_key, 'locked', expire) #①首先判断是否申请到了分布式锁
        yield locked
    finally:
        redis.delete(lock_key) #④当业务逻辑执行完成后，with 退出时会自动释放分布式锁，就不需要我们每次都手动释放锁了

# 业务调用 with 代码块执行结束后 自动释放锁资源
with lock(redis, 'locked', 3) as locked:
    if not locked:  #②如果申请失败，则业务逻辑直接返回
        pass 
    # do something ...
    #③如果申请成功，则执行具体的业务逻辑

#3.2 Redis事物和管道
from contextlib import contextmanager
@contextmanager
def pipeline(redis):
    pipe = redis.pipeline()
    try:
        yield pipe
        pipe.execute()
    except Exception as exc:
        pipe.reset()
            
# 业务调用 with 代码块执行结束后 自动执行 execute 方法
with pipeline(redis) as pipe:
    pipe.set('key1', 'a', 30)
    pipe.zadd('key2', 'a', 1)
    pipe.sadd('key3', 'a')

if __name__ == '__main__':
    pass

#####----------------------------------------------------------------------
#####-----------------------contextlib标准库实现----------------------------
from contextlib import AbstractContextManager, ContextDecorator
import functools
class _GeneratorContextManagerBase:

    def __init__(self, func, args, kwds):
        # 接收一个生成器对象 (方法内包含 yield 的方法就是一个生成器)
        self.gen = func(*args, **kwds)
        self.func, self.args, self.kwds = func, args, kwds
        doc = getattr(func, "__doc__", None)
        if doc is None:
            doc = type(self).__doc__
        self.__doc__ = doc

class _GeneratorContextManager(_GeneratorContextManagerBase,
                               AbstractContextManager,
                               ContextDecorator):

    def __enter__(self):
        try:
            # 执行生成器 代码会运行生成器方法的 yield 处
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield") from None

    def __exit__(self, type, value, traceback):
        # with 内没有异常发生
        if type is None:
            try:
                # 继续执行生成器
                next(self.gen)
            except StopIteration:
                return False
            else:
                raise RuntimeError("generator didn't stop")
        # with 内发生了异常
        else:
            if value is None:
                value = type()
            try:
                # 抛出异常
                self.gen.throw(type, value, traceback)
            except StopIteration as exc:
                return exc is not value
            except RuntimeError as exc:
                if exc is value:
                    return False
                if type is StopIteration and exc.__cause__ is value:
                    return False
                raise
            except:
                if sys.exc_info()[1] is value:
                    return False
                raise
            raise RuntimeError("generator didn't stop after throw()")
def contextmanager(func):
    @functools.wraps(func)
    def helper(*args, **kwds):
        return _GeneratorContextManager(func, args, kwds)
    return helper

class closing(AbstractContextManager):
    def __init__(self, thing):
        self.thing = thing
    def __enter__(self):
        return self.thing
    def __exit__(self, *exc_info):
        self.thing.close()