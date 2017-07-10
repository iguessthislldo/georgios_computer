#ifndef REGISTERS_HEADER
#define REGISTERS_HEADER

#include <memory>
#include <exception>
#include <string>
#include <vector>

#include "word.h"

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

class Register {
private:
    string _name;
    word _value;
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

    word value() {
        return _value;
    }

    half_word half_value(bool upper) {
        half_word bytes[2] = {0, 0};
        full_to_half(&bytes[0], &_value);
        return bytes[upper];
    }

    word value(word value) {
        return _value = value;
    }

    word half_value(half_word value, bool upper) {
        half_word bytes[2] = {0, 0};
        full_to_half(&bytes[0], &_value);
        bytes[upper] = value;
        half_to_full(&_value, &bytes[0]);
        return _value;
    }

    void program_set_value(word value) {
        if (!read_only) {
            _value = value;
        }
    }
};

class Registers {
private:
    std::vector<Register> registers;
    bool finalized = false;
    unsigned _special;

public:
    Register & operator[] (unsigned i) {
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

    size_t size() {
        return registers.size();
    }
};

#endif
