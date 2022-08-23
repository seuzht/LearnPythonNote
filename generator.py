'''
@description: iterable_object, iterator and generator
@author:Denn Zhang
@date:2022/08/22
'''

#!/usr/bin/env python

#1.可迭代对象iterable和迭代器iterator
##1.1 可迭代对象iterable并不是指某种具体的数据类型,它是指存储了元素的一个容器对象,且容器中的元素可以通过__iter__()方法或__getitem__()方法访问;
    ### 1.1.1__iter__方法的作用是让对象可以用for-in循环遍历,getitem()方法是让对象可以通过'实例名[index]'的方式访问实例中的元素;这两个方法的目的是Python实现一个通用的外部可以访问可迭代对象内部数据的接口;
    ### 1.1.2一个可迭代对象是不能独立进行迭代的,Python中,迭代是通过for-in来完成的;凡是可迭代对象都可以直接用for-in循环访问,这个语句其实做了两件事:第一件事是调用__iter__()获得一个迭代器,第二件事是循环调用__next__();
        # it = iter(itratable)
        # while True:
        # try:
        #   next(it)
        # except StopIteration:
        #   return
    ### 1.1.3常见的可迭代对象包括：
        #a) 集合数据类型,如list、tuple、dict、set、str等;
        #b) 生成器(generator),包括生成器和带yield的生成器函数(generator function),下节专门介绍;
    ### 1.1.4如何判断一个对象是可迭代对象呢？可以通过collections模块的Iterable类型判断,具体判断方法如下:
        #  from collections import Iterable #导入Iterable 模块
        #  isinstance(变量,Iterable) #判断一个变量是否为可迭代对象返回True表明是可迭代对象
    ### ref https://blog.csdn.net/laoyuanpython/article/details/94361908
    ### ref https://zhuanlan.zhihu.com/p/51610062
##1.2 迭代器是一个数据结构,也是一个对象,一种特殊的可迭代对象,通俗地说 iterator = iterable_obj + __next__(); iter(iterable_obj)可以将可迭代对象转换为迭代器;
    ### 迭代器是可以直接调用__next__独立遍历运行的;而可迭代对象只能借助于for-in进行遍历;
    ### 迭代器相对可迭代对象for-in来说没有其他作用,它主要是为生成器generator提供基础;
##1.3 迭代器会保存一个指针,指向可迭代对象的当前元素;调用 next 函数的时候,会返回当前元素,并将指针指向下一个元素;当没有下一个元素的时候,它会抛出StopIteration异常;
    ### 作为生成器的基础,它的使用可以减少内存占用;
    ### 迭代器是一个惰性序列; ref https://blog.csdn.net/Solo95/article/details/78834041


#2.生成器generator
##2.1生成器也是函数,函数中只要有 yield 关键字,那么它就是生成器函数,返回值为生成器对象;
    ###但yield不能和return共存,并且 yield 只能定义在函数中;
    ###当我们调用这个函数的时候,函数内部的代码并不立即执行,这个函数只是返回一个生成器对象;
    ###当我们使用for-in或者next()对其进行迭代的时候,函数内的代码才会被执行;
##2.2生成器对象存在 __iter__ 和 __next__ 这两种方法,因此它是一个迭代器;
    ###生成器对象知道如何保存执行上下文。它可以被无限次调用，每次都会生成序列的下一个元素。
##2.3生成器函数的特点：
    ###生成器函数执行的时候并不会执行函数体；
    ###当next生成器的时候,会从当前代码执行到之后的第一个 yield,会弹出值并暂停函数;
    ###当再次next生成器的时候,从上次暂停处开始向下执行;
    ###当没有多余 yield 的时候,会抛出 StopIteration 异常,异常的 Value 是函数的返回值;
    ###使用基于生成器的数据缓存区,可以允许第三方暂停、恢复和停止生成器,在开始这个过程之前无需导入所有数据以减少内存占用;
    ###生成器可以利用next函数于调用的代码进行交互。yield变成了一个表达式,yield表达式返回值(注意不是yield返回值)可以通过send方法传递;
        ####如果使用send启动（也就是第一次执行）生成器,必须使用None作为其参数,因为此时还没有yield能够接收它的值（毕竟接收该值的语句还没有开始执行）。
        ####或者第一次启动不用send而是用Next(gen)
##2.4生成器普通用法:递归
def fibonacci():#生成器函数
    a,b = 0,1
    while(True):
        yield b #返回b并暂停
        a,b = b,a+b
f = fibonacci() #调用生成器函数返回一个生成器对象
next(f) #或者 for-in f 遍历取值

def make_inc():#对生成器函数包装next,返回lambda函数对象,可以在使用上省略next,且可以像函数调用一样写法
    def counter():
        x = 0
        while True:
            x += 1
            yield x
    c = counter()
    return lambda: next(c)
f = make_inc() 
f()

##2.6生成器高级用法:协程 ref https://blog.csdn.net/u014257214/article/details/117433239
###进程和线程的调度是通过操作系统完成的，但是协程的调度是由用户态，也就是用户进行的。
###一旦函数执行到 yield 之后，它会暂停，暂停也就意味着让出 cpu 了。那么接下来就由用户决定执行什么代码。
###协程是为非抢占式多任务产生子程序的计算机程序组件，协程允许不同入口点在不同位置暂停或开始执行程序。
###从本质上而言，协程并不属于语言中的概念，而是编程模型上的概念。
'''Python3之前没有原生协程，只有基于生成器的协程
1.pep 342(Coroutines via Enhanced Generators)增强生成器功能
2.生成器可能通过 yield 暂停执行和产出数据
3.同时支持send()向生成器发送数据和throw()向生成器抛出异常

协程注意点
1.协程需要使用send(None)或者next(coroutine)来预激(prime)才能启动
2.在yield处协程会暂停执行
3.单独的yield value会产出值给调用方
4.可以通过 coroutine.send(value)来给协程发送值，发送的值会赋值给 yield表达式左边的变量value = yield
5.协程执行完成后（没有遇到下一个yield语句）会抛出StopIteration异常
'''
#2.6.1协程装饰器
#避免每次都要用 send 预激它,可以对生成器函数加上如下装饰器:
from functools import wraps
def coroutine(func):  
	#装饰器：向前执行到一个 `yield` 表达式，预激 `func` 
	@wraps(func)
	def primer(*args, **kwargs):   # 1
		gen = func(*args, **kwargs)  # 2
		next(gen)  # 3  #这样就不用每次都用 send(None) 启动了
		return gen  # 4
	return primer
#2.6.2python3原生协程
#python3.5引入 async/await支持原生协程(native coroutine)
import asyncio
import datetime
import random

async def display_date(num, loop):
	end_time = loop.time() + 50.0
	while True:
		print('Loop: {} Time: {}'.format(num, datetime.datetime.now()))
		if (loop.time() + 1.0) >= end_time:
			break
		await asyncio.sleep(random.randint(0, 5))

loop = asyncio.get_event_loop()
asyncio.ensure_future(display_date(1, loop))
asyncio.ensure_future(display_date(2, loop))
loop.run_forever()
