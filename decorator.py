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
#装饰器是一个可调用命名对象(不允许是lambda表达式),在被(装饰对象)调用时(运行期)接受单一参数fn或者cls，并返回一个可调用对象(函数/类) √
#任何可调用对象都可以作为装饰器(函数或者实现了__call__的类)
#装饰器分类：
###1.装饰器所修饰的对象是函数还是类:
      #1.1所修饰的对象是函数就是在运行期修改或扩展函数方法的功能;
      #1.2所修饰的对象是类就是在运行期修改类的属性和方法;
###2.装饰器本身的类型是函数还是类
      #2.1函数类型的装饰器本质就是利用fn和cls来接收被装饰函数/类，在利用wrapper(*args,**kw)来接收被装饰函数的参数;底线是装饰器需要定义fn/cls入参来接收被装饰对象
      #2.2类本身作为装饰器，需要类中定义__call__;类中的方法作为装饰器,跟函数装饰器一样，需要考虑第一个参数是否为self;
#装饰器带参：传递给装饰器的参数只被处理一次，即在函数声明并被装饰时（编译期）处理。与之相反，传递给函数的参数在该函数被调用时（运行时）处理


#装饰器定义核心：定义一个函数用于接受被修饰函数对象fn，然后用一个内部wrapper接受被修饰函数的参数*args,**kwargs;回调fn(*args,**kwargs)；最后返回这个wrapper
#装饰器用法核心：在定义体中对fn/cls、args和kwargs或者fn输出结果做文章，扩展功能;
'''#第一部分
------------------------------------------装饰器语法详解----------------------------------------
'''

''' 类型1:
------------------------------------------------------
函数型装饰器修饰函数
------------------------------------------------------
'''
#无参数的装饰器函数-------装饰(扩展)一个函数
def decoratorFnWithoutParas(fn):
    print('无参函数装饰器------ 调用')
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
#无参类装饰器,包装函数从__init__传入
class DecoratorClassWithoutParas(object):
    def __init__(self,fn): #无参数类装饰器在类初始化时传入所修饰的函数对象
        print('无参类装饰器---init调用.....')
        self.fn = fn
    def __call__(self,*args,**kwargs):#魔法方法__call__实现所修饰函数的调用
        print('无参类装饰器---—__call__执行.....')
        return self.fn(*args,**kwargs)
#带参类装饰器,装饰器参数从__init__传入,包装函数从__call__传入
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


#被修饰对象
decoratorFnInClass = DecoratorFnInClass()
#多个装饰器执行顺序：decoratorOuter(decoratorInner(originalFn))
###1.装饰器定义准备从上到下（传入fn前）
###2.装饰器调用（传入fn后)从下到上   √
###3.装饰器回调函数执行（wrapper 传入*args和**kwargs后)从上到下
@DecoratorFnInClass.decorator #类中定义的函数(成员函数/类函数)也可以作为函数型装饰器，只要符合函数型装饰器定义规则
@DecoratorClassWithoutParas
@decoratorFnWithParas2(level='WARNING')
@decoratorFnWithParas(level='INFO')  
@decoratorFnWithoutParas
def ordFunc(iNum,outStr):
    print("被修饰函数本地执行:iNum: {}  outStr: {}".format(iNum,outStr))


'''#第二部分
---------------------------------------装饰器应用场景-------------------------------------------
@1.类方法/静态方法
@2.参数检查
@3.权限检查
@4.输出格式化
@5.日志
@6.异步任务
@7.函数注册
@8.缓存
@9.代理
@10.上下文提供者
'''
#1.类中方法修饰：类方法 @classmethod  #静态方法 @staticmethod 
    ###详见 https://github.com/seuzht/LearnPythonNote/blob/master/descriptor.py
#2.1参数检查1@requires_ints
def requires_ints(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kwargs): #args是元组，kwargs是字典
        print('args is {0} ; kwargs is {1}'.format(args,kwargs))
        kwargs_values = [i for i in kwargs.values()]
        for arg in list(args) + kwargs_values:
            if not isinstance(arg,int): #函数参数类型检查
                raise TypeError('%s only accepts integers as arguments.' %fn.__name__)
    return wrapper
#2.2参数检查2+函数注册
rpc_info = {}
def xmlrpc(in_=(),out=(type(None),)):#带参数的装饰器
    def _xmlrpc(fn):
        #函数签名注册
        func_name = fn.__name__
        rpc_info[func_name] = (in_,out)
        def _check_types(elements,types):
            '''用来检查类型的子函数'''
            if len(elements) != len(types):
                raise TypeError('argument count is wrong')
            typed = enumerate(zip(elements,types))
            for index , couple in typed:
                arg , of_the_right_type = couple
                if isinstance(arg,of_the_right_type):
                    continue
                raise TypeError('arg #%d should be %s' %(index,of_the_right_type))
        #包装过的函数
        def __xmlrpc(*args):#没有允许的关键词
            #检查输入的内容
            checkable_args = args[1:] #去掉self
            _check_types(checkable_args,in_)
            #运行函数
            res= function(*args)
            #检查输出的内容
            if not type(res) in (tuple,list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res,out)
            #函数及其类型检查成功
            return res
        return __xmlrpc
    return _xmlrpc
class RPCView:
    @xmlrpc((int,int)) #类型转换 two int -> None
    def meth1(self,int1,int2):
        print('received %d and %d' %(int1,int2))
    @xmlrpc((str,),(int,)) #类型转换 string -> int
    def meth2(self,phrase):
        print('received %s' %phrase)
        return 12
#3.权限检查@login_required @permission_required
class User(object):
    def __init__(self,username,email):
        self.username = username
        self.email = email
class AnonymousUser(User):#匿名用户
    def __init__(self):
        self.username = None
        self.email = None
    def __nonzero__(self):#匿名用户不通过
        return False
def requires_user(fn):#验证当前用户是否有效
    @functools.wraps(fn)
    def wrapper(user,*args,**kwargs):#包装函数或静态方法，不能包装绑定到类中的实例方法，因为第一个参数是user
        if user and isinstance(user,User): #匿名用户__nonzero__返回false；其他用户判断是否是User实例
            return fn(user,*args,**kwargs)
        else:
            raise ValueError('A valid user is required to run this.')
    return wrapper
#4.1输出格式化 JSON格式
import json
def json_output(fn):
    @functools.wraps(fn)
    def wrapper(*args,**kwargs):
        result = fn(*args,**kwargs)
        return json.dumps(result)#将原函数输出序列化为标准的JSON格式
#4.2捕获特定异常并以指定格式的JSON输出，而不是让异常冒泡并回溯
class JSONOutputError(Exception):
    def __init__(self,message):
        self._message = message
    def __str__(self):
        return self._message
def json_outputWithCatchException(fn):
    def wrapper(*args,**kwargs):
        try:
            result = fn(*args,**kwargs)
        except JSONOutputError as ex: #被修饰函数执行发生异常时异常对象ex
            result = {
                'status':'error',
                'message':'str(ex)'#调用JSONOutputError的__str__方法处理
            }
        return json.dumps(result)
    return wrapper
#5.日志 @log
import logging
import time
def logged(fn):
    def wrapper(*args,**kwargs):
        start =time.time()
        return_value = fn(*args,**kwargs)
        #添加日志
        end = time.time()
        delta = end - start
        logger = logging.getLogger('decorator.logged')
        logger.warn('Called method %s at %.02f; execution time %.02f '
                    'seconds; result %r.' %
                    (fn.__name__, start, delta,return_value))
        #
        return return_value
    return wrapper
#6.异步任务 @task
class Task(object):
    def run(self,*args,**kwargs):
        raise NotImplementedError('Subclasses must implement run.')
    def identity(self):
        return 'I am a task'
    def __call__(self,*args,**kwargs): #该类实例可被调用
        return self.run(*args,**kwargs)
def task(fn):#@task装饰器
    class TaskSubclass(Task):
        def run(self,*args,**kwargs):
            #实现异步
            return fn(*args,**kwargs)
    return TaskSubclass() #使得被修饰的函数对象可以直接像decoratorFn()这样调用
#7.函数注册 @register 在装饰器中将接收到(被修饰)的fn注册到字典或列表中
class Register(object):
    def __init__(self):
        self._registry = []
    def register(self,fn): #装饰器函数，用法为@Register().register
        self._registry.append(fn)
        return fn
    def run_all(self,*args,**kwargs):
        return_values = []
        for f in self._registry:
            return_values.append(f(*args,**kwargs))
        return return_values
#8.缓存：缓存装饰器与参数检查十分相似，不过它重点时关注那些内部状态不会影响输出的函数。每组参数都可以链接到唯一的结果。函数式编程functional programming
#缓存装饰器可以将输出与计算它所需要的参数放在一起，并在后续的调用中直接返回它。这种行为称为memoizing(备忘);
#缓存代价高昂的函数可以显著提高程序的总体性能;缓存值还可以与函数本身绑定，以管理其作用域和生命周期，代替集中化的字典;
#任何情况下优先使用基于高效缓存算法的专用缓存库;
import time
import hashlib
import pickle

cache = {} #双层字典 key所映射的值也是字典{'value':result,'time':time.time()}
def is_obsolete(entry,duration):
    return time.time() - entry['time'] > duration
def compute_key(fn,args,kw):
    key = pickle.dumps((fn.__name__,args,kw))# https://blog.csdn.net/weixin_38145317/article/details/93190204
    return hashlib.sha1(key).hexdigest()#https://blog.csdn.net/Owen_goodman/article/details/111950637
def memoize(duration=10):
    def _memoize(fn):
        def __memoize(*args,**kw):
            key = compute_key(fn,args,kw)
            #判断是否已经拥有
            if (key in cache and not is_obsolete(cache[key],duration)):
                print('we got a winner')
                return cache[key]['value']
            #计算
            result = function(*args,**kw)
            #保存结果
            cache[key] = {
                'value':result,
                'time':time.time()
            }
            return result
        return __memoize
    return _memoize
#9.代理:使用全局机制来标记和注册函数;
#包含函数注册和用户权限检查
class User(object):
    def __init__(self,roles): #roles是个元组
        self.roles = roles
class Unauthorized(Exception):
    pass
#这一模型常用于web框架中，用于定义可发布类的安全性（修饰实例方法的安全性）
def protect(role): 
    def _protect(fn):
        def __protect(*args,**kw):#因为包装的函数对象时类中的实例方法，所以self作为args的第一个参数传入
            user = globals().get('user')#获取当前用户全局变量
            if user is None or role not in user.roles:
                raise Unauthorized("I won't tell u")
            return fn(*args,**kw)#args的第一个参数作为self使用
        return __protect
    return _protect
tarek = User(('admin','user'))#
bill = User(('user',))
class MySecrets(object):
    @protect('admin')#指定waffle_recipe实例方法的访问安全性
    def waffle_recipe(self):
        print('use tons of butter!')
these_are = MySecrets()
user = tarek #指定tarek为当前用户全局变量
these_are.waffle_recipe()
#10.上下文提供者：上下文装饰器确保函数可以运行在正确的上下文环境中，或者在函数前后运行一些代码，以设定并复位一个特定的执行环境；
#e.g. 多线程同步锁
from threading import RLock
lock = RLock()

def synchronized(fn):
    def _synchronized(*args,**kw):
        lock.acquire()
        try:
            return fn(*args,**kw)
        finally:
            lock.release()
    return _synchronized
    
@synchronized
def thread_safe():#确保锁定资源
    pass



if __name__ == '__main__':
    ordFunc(0,"HELLO DECORATOR")
    #functionwithparas(1,'Dennis') #will raise a TypeError exception since 'Dennis' is a string but not a integer