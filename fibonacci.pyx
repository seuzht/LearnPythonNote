#cython作为语言对python的c扩展

'''利用cdef关键字声明为纯C函数,返回值和接受参数类型都是C语言类型;
可以解决静态类型参数声明与python对象之间递归转换问题;
'''

#声明为纯C,被递归调用时就不会转换为Python对象处理
cdef long long fibonacci_cc(unsigned int n) nogil: #nogil标记整个C风格函数是无GIL的安全调用
    if n < 2:
        return n
    else :
        return fibonacci_cc(n-1) + fibonacci_cc(n-2)

def fibonacci(unsigned int n)://静态类型参数
    #with nogil
    return fibonacci_cc(n)