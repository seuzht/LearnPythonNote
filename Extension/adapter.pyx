
''' C++ 头文件 demo.h
#ifndef DEMO_H
#define DEMO_H 
using namespace std;
namespace demo {
    class MyDemo {
        public:
            int a;
            MyDemo();
            MyDemo(int a );
            ~MyDemo(); 
            int mul(int m );
            int add(int b);
            void sayHello(char* name);
    };
}
#endif
'''
''' C++ 实现文件 demo.cpp
#include "demo.h" 
#include <iostream> 

namespace demo {
 
    MyDemo::MyDemo () {}
 
    MyDemo::MyDemo (int a) {
        this->a = a; 
    }
 
    MyDemo::~MyDemo () {}
 
    int MyDemo::mul(int m) {
        return this->a*m;
    }
 
    int MyDemo::add (int b) {
        return this->a+b;
    }
    void MyDemo::sayHello(char* name){
        cout<<"hello "<<name<<"!"<<endl;
    }  
}
'''

# adpater.pyx 创建PyMyDemo类用于将C/C++代码做一层封装,使得Python能直接调用
# distutils: language = c++ 指定当前文件生成C++文件
from cdemo cimport MyDemo

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class PyMyDemo:
    cdef MyDemo c_mydemo  # Hold a C++ instance which we're wrapping

    def __cinit__(self,a):
        self.c_mydemo = MyDemo(a)   
    def mul(self, m):
        return self.c_mydemo.mul(m)

    def add(self,b):
        return self.c_mydemo.add(b)

    def sayHello(self,name ):
        self.c_mydemo.sayHello(name) 


