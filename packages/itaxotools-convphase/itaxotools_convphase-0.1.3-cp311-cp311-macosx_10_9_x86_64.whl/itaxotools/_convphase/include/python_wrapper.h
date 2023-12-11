#ifndef PYTHON_WRAPPER_H
#define PYTHON_WRAPPER_H

#include <Python.h>
#include <vector>
#include <string>
#include <stdexcept>

class ProgressCallbackError : public std::runtime_error {
public:
    ProgressCallbackError()
        : std::runtime_error("progress callback error") {}
};

struct InputLine{
	std::string id;
	std::string data;
};

struct OutputLine{
	std::string id;
  std::string data_a;
	std::string data_b;
};

struct OutputLinesObject{
    PyObject_HEAD
    std::vector<OutputLine> lines;
    int current;
} ;

static PyObject* py_setProgressCallback(PyObject* self, PyObject* args);
void py_progressReporter(int value, int maximum, const char * text);

static PyObject* py_seqPhaseStep1(PyObject* self, PyObject* args);
static PyObject* py_phase(PyObject* self, PyObject* args);
static PyObject* py_seqPhaseStep2(PyObject* self, PyObject* args);
static PyObject* py_convPhase(PyObject* self, PyObject* args);
static PyObject* py_iterPhase(PyObject* self, PyObject* args);

static PyObject* OutputLines_new(PyTypeObject* type, PyObject* args, PyObject* kwargs);
static PyObject* OutputLines_iter(PyObject* self);
static PyObject* OutputLines_next(PyObject* self);

#endif
