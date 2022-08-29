#define PY_SSIZE_T_CLEAN
#include <Python.h>  //导入 Python API
 
/*
*@Description:基于Python/C API, C代码的Python扩展示例，使Python可以调用C代码接口
*@Author: Dennis Zhang
*@Date:2022/08/25
*/

#ref https://zhuanlan.zhihu.com/p/164598060

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

//原纯c代码接口
int fputs(const char *str, FILE *stream);
int main() {
    FILE *fp = fopen("write.txt", "w");
    fputs("I Love NightTeam!", fp);
    fclose(fp);
    return 1;
}

//暴露对外Python接口的定义
//c function extension which could be called by Python
static PyObject *fputs_py(PyObject *self, PyObject *args) {
    //str 是要写入文件流的字符串。
    //filename 是要写入的文件的名称。
    char *str, *filename = NULL;
    int bytes_copied = -1;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ss", &str, &filename)) {
        return NULL;
    }

    FILE *fp = fopen(filename, "w");
    bytes_copied = fputs(str, fp);
    fclose(fp);

    return PyLong_FromLong(bytes_copied); //将C接口返回的数据类型转换为Python可以识别的
}

static PyMethodDef FputsMethods[] = {
    {"fputs", fputs_c, METH_VARARGS, "Python interface for fputs C library function"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef fputsmodule = {
    PyModuleDef_HEAD_INIT,
    "fputs",
    "Python interface for the fputs C library function",
    -1,
    FputsMethods
};

PyMODINIT_FUNC PyInit_fputs(void) {
    return PyModule_Create(&fputsmodule);
}

/*模块构建
from distutils.core import setup, Extension

def main():
    setup(name="fputs",
          version="1.0.0",
          description="Python interface for the fputs C library function",
          author="dennis",
          author_email="seuzht@163.com",
          ext_modules=[Extension("fputs", ["fputsmodule.c"])])

if __name__ == "__main__":
    main()
*/