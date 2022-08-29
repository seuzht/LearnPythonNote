'''
@description: dive into how to use descriptor, classproperty/instanceproperty and staticmethod/classmethod/instancemethod 
@author: Dennis Zhang
@date:2022/08/12
属性管理方式:  _privateName ; __slot__ ; @property ; 描述符
'''
#!/usr/bin/env python3


#描述符类的作用：
#代理一个类的属性，让程序员在引用一个对象属性时自定义要完成的工作
#它是实现大部分Python类特性中最底层的数据结构的实现手段，是使用到装饰器或者元类的大型框架中的一个非常重要组件
#描述符协议对__get__和__set__的要求（object参数，并含有__dict__对象）可以看出，描述符可以修饰的对象及调用的方式；



#代理实例属性的描述符类，非共享实例属性,由调用者object的__dict__来保证非共享
class instancepropertydescriptor(object):
    def __init__(self,pname):
        self.pkey = pname
    def __get__(self,object,ownerType):
        return object.__dict__[self.pkey]
    def __set__(self,object,value):
        #可以补充自定义托管属性的管理逻辑
        object.__dict__[self.pkey] = value

'''
非数据描述符类可以修饰类方法，只需要实现__get__方法即可
下面是利用非数据描述符来实现装饰器@staticmethod和@classmethod
既是描述符又是装饰器
__get__与__call__实现装饰器方式有何区别？？？
'''
#修饰静态方法的非数据描述符类,实现一个装饰器@staticmethoddescriptor
class staticmethoddescriptor(object):
    def __init__(self,fn):
        self.fn = fn
    def __get__(self,object,ownerType):
        return self.fn

#修饰类方法的非数据描述符类，实现一个装饰器@classmethoddescriptor
class classmethoddescriptor(object):
    def __init__(self,fn):
        self.fn = fn
    def __get__(self,object,ownerType):
        def newfn(*args):
            return self.fn(ownerType,*args)
        return newfn


#延迟求值属性：将类属性的初始化延迟到被实例访问时
class initonaccess(object):
    def __init__(self,klass,*args,**kwargs): #klass是针对类属性初始化的逻辑处理方法
        self.klass = klass
        self.args = args
        self.kwargs = kwargs
        self._initialized = None #类属性初始化处理后的结果
    def __get__(self,object,ownerType):
        if self._initialized == None:
            print('initialized')
            self._initialized = self.klass(*self.args,**self.kwargs)
        else:
            print('cached！')
        return self._initialized

#实例对象需要被保存为实例之间共享的类属性，以节约资源
#在全局导入时实例对象不能被初始化，因为其创建过程依赖某个全局应用状态/上下文
#用来修饰一个实例方法,把实例方法变成一个实例属性来使用；
#@property装饰器可以把一个实例方法修饰成实例属性来使用，但不是真正的实例属性，因为__dict__中没有；
#lazyproperty描述符可以将一个实例方法变成一个真正的实例属性；所以只有在第一次调用时进行一次计算，而之后每次调用不会重复计算，会直接从__dict__中查找；
#https://www.jianshu.com/p/708dc26f9b92
class lazyproperty(object):
    def __init__(self,function) -> None:
        self.fget = function
    def __get__(self,object,ownerType):
        value = self.fget(object)
        #setattr(object, name, value)
        setattr(object,self.fget.__name__,value) 
        return value

# https://zhuanlan.zhihu.com/p/28010894
class myclass(object):
    myclassproperty = "classproperty"
    #下面是经描述符修饰的实例属性，类无法直接访问
    paras = instancepropertydescriptor('paras')  #传入描述符内部属性名称存储,作为后面访问属性时实例对象字典__dict__的key
    def __init__(self,value='xxx'):
        self.paras = value  #给描述符内部字典的key添加对应value
    
    #静态方法就是全局，不属于类，也不属于实例，碰巧写在类中，类和实例都可以访问调用
    #staticmethod装饰器或描述符可以忽略类/实例对象调用时传入的self和cls参数，使其使用方式上保持静态特性；
    #静态方法内无法访问类属性和实例属性，可以使用传入参数
    @staticmethoddescriptor
    def staticfn(paras): 
        print('this is a staticfn %s' %paras)

    #未修饰的静态方法，不是真正意义上的静态方法，只能被类调用，不能被实例对象调用；
    #不能访问类属性和实例属性，可以使用传入参数
    def nonstaticmethodfn(paras):
        print('this is no staticmethod fn %s' %paras)
    

    #类方法，跟静态方法一样，类和实例都可以调用；但区别是静态方法无cls和self，而类方法无self有cls，
    #cls参数决定了在类方法内部只能访问类所拥有的属性，不能访问实例属性
    #经过classmethod装饰器修饰可以让类调用时提供类本身作为cls参数传入，在实例调用时也提供实例的类型作为cls参数传入，使其保持类方法的特性；
    #类方法与类属性有点不同的是，不同的实例对象调用类方法是一样的，而不同的实例对象所拥有的类属性是不同的拷贝；
    #如果没有classmethod修饰，则这个classfn(cls)就是一个实例方法而不是类方法，self当作cls参数传入；类不可以调用；
    @classmethod
    def classfn(cls):
        print("this is a classfn")
        #print('classfn paras is %s' %cls.paras) 类无法访问经过描述符修饰的实例属性
        print('classfn paras is %s' %cls.myclassproperty) #类可以访问类属性

    #实例方法，只能实例对象调用；
    def instancefn(self):
        print('this is a instancefn')
        print('instancefn paras is %s' %self.paras)

if __name__ == '__main__':
    mm = myclass('value')  #传入描述符内部字典的value
    print('BEFORE mm _dict__ is %s' %mm.__dict__)
    mm.paras = 'dennis' #描述符实例属性，只能由实例对象访问
    print('mm paras is %s' %mm.paras)
    print('AFTER mm _dict__ is %s' %mm.__dict__)

    print('=========================') 

    myclass().instancefn()#实例方法只能由实例对象调用

    print('=========================') 

    myclass.nonstaticmethodfn('nonstaticmethodfn') #无staticmethod修饰的静态方法，只能被类调用；跟类方法类似，不是真正意义上的静态方法
    
    print('=========================') 
    
    myclass.staticfn('newparasvalue')#staticmethod装饰器在类对象调用时忽略cls，让类对象可以调用静态方法
    myclass().staticfn('newparasvalue')#staticmethod装饰器在实例对象调用时忽略self，让实例对象也可以调用静态方法
    #print('类属性值 %s' %myclass.paras) 错误，被描述符修饰成实例属性了，类无法直接访问，因为类无__dict__，只有实例化后才有__dict__
    print('实例属性值 %s' %myclass('value').paras)
    
    print('=========================') 
    
    m = myclass('objectpara')
    m2 = myclass('objectpara')
    #有classmethod修饰时的类方法，类和实例都可以调用
    print(m.classfn == m2.classfn) #实例调用类方法跟类调用类方法是一致的，都是同一份内存
    print(m.classfn == myclass.classfn) #实例调用类方法跟类调用类方法是一致的，都是同一份内存
    m.classfn() 
    myclass.classfn()
    