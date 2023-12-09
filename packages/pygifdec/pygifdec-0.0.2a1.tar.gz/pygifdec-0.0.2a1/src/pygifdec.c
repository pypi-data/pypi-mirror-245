#include <Python.h>
#include <object.h>
#include "gifdec.h"

typedef struct GIF
{
    PyObject_HEAD;
    Py_ssize_t size;
    PyObject *width;
    PyObject *height;
    PyObject *depth;
    PyObject *bgcolor;
    gd_GIF *gd_GIF_ptr;
} GIF;

static PyObject *GIF_close(PyObject *self, PyObject *args)
{
    GIF *gif = (GIF *)self;
    gd_close_gif(gif->gd_GIF_ptr);
    Py_XDECREF(gif->width);
    Py_XDECREF(gif->height);
    Py_XDECREF(gif->depth);
    Py_XDECREF(gif->bgcolor);
    Py_RETURN_NONE;
}

static PyObject *GIF_make_bgcolor(PyObject *self, PyObject *args)
{
    GIF *gif = (GIF *)self;
    gd_GIF *g = gif->gd_GIF_ptr;
    uint8_t *colors = &g->gct.colors[g->bgindex * 3];
    PyObject *pyColors = Py_BuildValue("(BBB)", colors[0], colors[1], colors[2]);
    return pyColors;
}

unsigned char *parse_args_frame_bytearray(GIF *self, PyObject *args)
{
    PyObject *byteObj;
    if (!PyArg_ParseTuple(args, "O", &byteObj))
    {
        return NULL;
    }

    if (!PyByteArray_Check(byteObj))
    {
        PyErr_SetString(PyExc_TypeError, "Expected a bytearray object");
        return NULL;
    }

    unsigned char *data = (unsigned char *)PyByteArray_AsString(byteObj);
    if (data == NULL)
    {
        return NULL;
    }
    Py_ssize_t length = PyByteArray_Size(byteObj);
    if (length != self->size)
    {
        PyErr_SetString(PyExc_TypeError, "bytearray length must mutch the frame");
        return NULL;
    }
    return data;
}

static PyObject *GIF_render_frame(PyObject *self, PyObject *args)
{
    GIF *gif = (GIF *)self;
    unsigned char *data = parse_args_frame_bytearray(gif, args);
    gd_render_frame(gif->gd_GIF_ptr, data);
    Py_RETURN_NONE;
}

static PyObject *GIF_get_frame(PyObject *self, PyObject *args)
{
    GIF *gif = (GIF *)self;
    int ret = gd_get_frame(gif->gd_GIF_ptr);
    return Py_BuildValue("i", ret);
}

static PyMethodDef GIF_methods[] = {
    {"close", GIF_close, METH_NOARGS, "close the gif"},
    {"render_frame", GIF_render_frame, METH_VARARGS, "render a gif"},
    {"get_frame", GIF_get_frame, METH_VARARGS, "get a new frame"},
    {NULL, NULL, 0, NULL}};

static PyObject *GIF_get_width(GIF *self, void *closure)
{
    Py_INCREF(self->width);
    return self->width;
}

static PyObject *GIF_get_height(GIF *self, void *closure)
{
    Py_INCREF(self->height);
    return self->height;
}

static PyObject *GIF_get_depth(GIF *self, void *closure)
{
    Py_INCREF(self->depth);
    return self->depth;
}

static PyObject *GIF_get_bgcolor(GIF *self, void *closure)
{
    Py_INCREF(self->bgcolor);
    return self->bgcolor;
}

static PyObject *GIF_get_size(GIF *self, void *closure)
{
    return Py_BuildValue("i", self->size);
}

static PyGetSetDef GIF_getset[] = {
    {"width", (getter)GIF_get_width, NULL, "GIF width", NULL},
    {"height", (getter)GIF_get_height, NULL, "GIF height", NULL},
    {"depth", (getter)GIF_get_depth, NULL, "GIF depth", NULL},
    {"bgcolor", (getter)GIF_get_bgcolor, NULL, "GIF bgcolor", NULL},
    {"size", (getter)GIF_get_size, NULL, "GIF size", NULL},
    {NULL, NULL, NULL, NULL, NULL}};

static PyTypeObject PyGIF = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "pygifdec.GIF",
    .tp_basicsize = sizeof(GIF),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "GIF object",
    .tp_methods = GIF_methods,
    .tp_getset = GIF_getset,
};

static PyObject *open_gif(PyObject *self, PyObject *args)
{
    const char *fname;
    if (!PyArg_ParseTuple(args, "s", &fname))
    {
        return NULL;
    }
    gd_GIF *gif = gd_open_gif(fname);
    if (gif == NULL)
    {
        Py_RETURN_NONE;
    }

    GIF *result = (GIF *)PyObject_New(GIF, &PyGIF);
    result->gd_GIF_ptr = gif;
    result->size = gif->width * gif->height * 3;
    result->width = Py_BuildValue("i", gif->width);
    result->height = Py_BuildValue("i", gif->height);
    result->depth = Py_BuildValue("i", gif->depth);
    result->bgcolor = GIF_make_bgcolor((PyObject *)result, NULL);
    return (PyObject *)result;
}

static PyMethodDef methods[] = {
    {"open", open_gif, METH_VARARGS, "open a GIF object"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef pygifdec = {
    PyModuleDef_HEAD_INIT, "pygifdec", NULL, -1, methods};

PyMODINIT_FUNC PyInit_pygifdec(void)
{
    PyObject *module = PyModule_Create(&pygifdec);
    if (PyType_Ready(&PyGIF) < 0)
        return NULL;

    Py_INCREF(&PyGIF);
    PyModule_AddObject(module, "GIF", (PyObject *)&PyGIF);

    return PyModule_Create(&pygifdec);
}
