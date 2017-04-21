#ifndef REGISTERS_HEADER
#define REGISTERS_HEADER

#include <memory>
#include <exception>
#include <string>
#include <vector>

using std::string;
using std::to_string;

class Register_Exception : public std::exception {
private:
    string message;
public:
    Register_Exception(const string & message) {
        this->message = message;
    }

    const char * what () const throw () {
        return message.c_str();
    }
};

template <class T>
class Register {
private:
    string _name;
    T _value;
    bool read_only;
public:
    Register(const string & name, bool read_only) {
        _name = name;
        this->read_only = read_only;
    }

    string name() {
        return _name;
    }

    void name(const string & name) {
        _name = name;
    }

    T value() {
        return _value;
    }

    T value(unsigned value) {
        _value = value;
        return value;
    }

    void program_set_value(T value) {
        if (read_only) {
            throw Register_Exception(
                string("Attempt to write read only register: ") + _name
            );
        } else {
            _value = value;
        }
    }
};

template <class T>
class Registers {
private:
    std::vector<Register<T>> registers;
    bool finalized = false;
    unsigned _special;

public:
    Register<T> & operator[] (unsigned i) {
        if (!finalized) {
            throw Register_Exception("Registers are not finialized");
        }
        return registers[i];
    }

    unsigned add_ro_reg(const string & name) {
        if (finalized) {
            throw Register_Exception("Registers are already finialized");
        }
        unsigned index = registers.size();
        registers.emplace_back(name, true);
        return index;
    }

    unsigned add_rw_reg(const string & name) {
        if (finalized) {
            throw Register_Exception("Registers are already finialized");
        }
        unsigned index = registers.size();
        registers.emplace_back(name, false);
        return index;
    }

    void finalize(unsigned total) {
        if (finalized) {
            throw Register_Exception("Registers are already finialized");
        }
        if (registers.size() > total) {
            throw Register_Exception("More special registers than specified");
        }
        _special = registers.size();
        for (unsigned i = _special; i < total; i++) {
            registers.emplace_back(to_string(i - _special), false);
        }
        finalized = true;
    }
};

#endif
