%module(package="tmGrammar" moduleimport="import $module") tmGrammar

%include <std_vector.i>
%include <std_string.i>
%include <std_map.i>

namespace std {
  %template(StringVector) vector<string>;
  %template(map_string_int) map<string, int>;
}

%{
#define SWIG_FILE_WITH_INIT
#include "tmGrammar/Algorithm.hh"
#include "tmGrammar/Cut.hh"
#include "tmGrammar/Object.hh"
#include "tmGrammar/Function.hh"
%}

%rename(Algorithm_Logic) Algorithm::Logic;
%rename(Algorithm_parser) Algorithm::parser;

%rename(Cut_Item) Cut::Item;
%rename(Cut_parser) Cut::parser;

%rename(Object_Item) Object::Item;
%rename(Object_Unknown) Object::Unknown;
%rename(Object_parser) Object::parser;

%rename(Function_Item) Function::Item;
%rename(Function_parser) Function::parser;
%rename(Function_Unknown) Function::Unknown;
%rename(Function_getCuts) Function::getCuts;
%rename(Function_getObjects) Function::getObjects;
%rename(Function_getObjectCuts) Function::getObjectCuts;

%include "tmGrammar/Algorithm.hh"
%include "tmGrammar/Cut.hh"
%include "tmGrammar/Object.hh"
%include "tmGrammar/Function.hh"
