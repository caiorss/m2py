#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m2py.functional.hof import pluck, get
from pprint import pprint

class Person:

    # def __new__(self, name, age):
    #     self.name = name
    #     self.age = age

    def __init__(self,  name, age):
        print("Constructor 2")
        self.name = name
        self.age = age

    def say_name(self):
        print("My name is ", self.name, " My age is  ", self,age)



people = [{ 'name': 'moe', 'age': 40}, {'name': 'larry', 'age': 50}, {'name': 'curly', 'age': 60}]




name = pluck("name")
age = pluck("age")

pprint(name(people))
pprint(age(people))


peope_objects =  list(map( lambda d: Person(**d), people))
print(peope_objects)



# p = make_people(name="Hello", age=20)
# print(p.name)
# print(p.age)

pprint(name(peope_objects))
pprint(age(peope_objects))

print(list(map(get("name"), people)))
