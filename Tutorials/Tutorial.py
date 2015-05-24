# In this series of Python tutorials, I used Enthought Python Distribution:
# A scientific-oriented Python distribution from Enthought (http://www.enthought.com)
# This includes Enthought Canopy Express, a free base scientific distribution (with NumPy, 
# SciPy, matplotlib, Chaco, and IPython) that includes a comprehensive suite of more than 
# 100 scientific packages across many domains. In addition, you can also request an academic
# license by entering your Columbia email to gain access to an additional 150 packages and 
# a Graphical Package Manager with more than 14,000 community packages. The license is valid
# up to 1 year.
# I also leveraged Wes McKinney's book "Python for Data Analysis" if you are interested in 
# learning more about using Python for data munging, processing, and analyzing. 

# The basics:

# The Python language design is distinguished by its emphasis on readability and simplicity.
# Some people go so far as to liken it to "executable pseudocode"

# No.1 Whitespace in place of brace
# Python uses whitespace(tabs or spaces) to structure code, unlike we use braces in languages
# such as R. For instance:
for x in range(1,10):
    if x < 6:
        print True
    else:
        print False
# Here a colon denotes the start of an indented code block after which all of the code must be
# indented by the same amount until the end of the block; usually 4 spaces is the default indentation

# No.2 No statement termination
# In addition, Python statements do not need to be terminated by semicolons, unlike in C++.
# Semicolons, however, can be used to separate multiple statements on a single line:
a = 5; b = 6; c = 7

# No.3 Python Object
# An important characteristics of the Python language is the consistency of its object model. 
# In fact, every number, string, data structure, function, class, and module exists in the Python
# interpreter is referred to as a Python object. Each object has an associated type and internal data

# No.4 Comments
# As you might noticed, any text preceded by a hash mark(#) is ignored by the Python interpreter
# This is often used to add comments to code. 

# No.5 Variables and Pass-by-reference
# When assigning a variable in Python, you are essentially creating a reference to the object on the 
# right hand side of the equal sign. For instance:
a = [1,2,3]
b = a            # Assign a to a new variable b. In some languages, this assignment would cause the data [1,2,3] to be copied.
                 # In Python, however, a and b now refer to the same object, the original list [1,2,3]
a.append(4)
b                # Python outputs [1,2,3,4] instead of [1,2,3]

# In addition, when you pass objects as arguments to a function, you are only passing references; no copying occurs.
# Thus, Python is said to pass by reference. For instance:
def append_element(some_list, element):
    some_list.append(element)
data = [1,2,3]
append_element(data,5)
data            # Python outputs [1,2,3,5]

# To check if two references refer to the same object, use the 'is' keyword
# the 'is not' keyword is also valid if you want to check that two objects are not the same
a = [1,2,3]
b = a
c = list(a)   # list function always creates a new list

a is b       # Python outputs True because a and b refer to the same object [1,2,3]
a is c       # Python outputs False because a and c don't refer to the same object [1,2,3]
# Notice: This is not the same thing as compared with '==', because in this case we have:
a == c       # Python outputs True because a and c share the same values

# No.6 Strong Types
# Python is a strongly-typed language, which means that every object has a specific type(or class), and implicit conversions
# will occur only in certain obvious circumstances, such as:
a = 4.5
b = 2
print 'a is %s, b is %s' %(type(a),type(b))    # Python outputs 'a is <type 'float'>, b is <type 'int'>'
a/b             # Python outputs 2.25

# This example also illustrates that Python is a "typed language"
'5' + 5         # Python outputs a error message

# You can check that an object is an instance of a particular type using the 'isinstance' function
a = 5
isinstance(a, int)  # Python outputs True
# 'isinstance' can also accept a tuple of types if you want to check that an object's type is among those present in the tuple
a = 5
isinstance(a, (str, float))  # Python outputs False because a is an integer
  
# No.7 Imports
# In Python a module is simply a .py file that contains function and variable definitions along with 
# such things imported from other .py files. For example:
# some_module.py
PI = 3.14159

def f(x):
    return x + 2

def g(a, b):
    return a + b
    
# If we want to access the variables and functions defined in some_module.py, from another file in the 
# same directory we could do:
import some_module
result = some_module.f(6)
pi = some_module.PI
# Or equivalently:
from some_module import PI, f, g
result = g(2,PI)
# Using the 'as' keyword you could also give imports different variable names:
import some_module as sm
from some_module import PI as pi, g as gf
r1 = sm.f(pi)
r2 = sm.gf(8,pi)

# No.8 Mutable and imutable objects
# Most objects in Python are mutable, such as lists, dicts, NumPy arrays, or 
# most user-defined types(classes). This means that the object or value that they contain
# can be modified. For instance:
a_list = ['foo',2,[4,5]]
a_list[2] = (3,4)
a_list        # Python outputs ['foo', 2, (3, 4)]

# Others, like strings and tuples, are immutable
a_tuple = ('python',10, [4,5])
a_tuple[1] = 'four'
a_tuple      #  Python outputs error message 

# No.9 Strings
# You can write string literal using either single quotes ' or double quotes ":
a = 'one way of writing a string'
b = "another way"
# For multiline string with line breaks, you can use triple quotes, either ''' or """:
c = """
This is a longer string that 
spans multiple lines
"""
c       # Python outputs '\nThis is a longer string that \nspans multiple lines\n'

# As aforementioned, Python strings are immutable; you cannot modify a string without creating a new string
a = "this is a string"
a[2] = "e"     # Python outputs error message 
# However, 'replace' function could bypass string's immutability property
b = a.replace('string', 'longer string')
b              # Python outputs 'this is a longer string'
# Strings are a sequence of characters and therefore can be treated like other sequences, such as lists and tuples
s = 'python'
a = list(s)
a[:4]
# Add two strings together produce a new string
a = 'this is the first half'
b = ' and this is the second half'
a + b
# String with a % followed by one or more format characters is a target for inserting a value into that string. For instance;
a = '%.2f %s are worth $%d'
a % (4.5560, 'Argentine Pesos', 1)

# No.10 Booleans
# The two boolean values in Python are written as True and False.
# Boolean values are combined with the 'and' and 'or' keywords
True and False     # Python outputs False
False or True      # Python outputs True
# Most objects in Python have a notion of true or falseness. For instance, empty sequences are treated as False if used in control flow
# You can see exactly what boolean value an object takes on by invoking 'bool' on it:
bool([])           # Python outputs False
bool([1,2])        # Python outputs True
bool('Hello World!')  # Python outputs True
bool('')              # Python outputs False
bool(0)               # Python outputs False
bool(1)               # Python outputs True

# No.11 Dates and Times
# The built-in Python datetime module provides datetime, date, and time types
from datetime import datetime, date, time
dt = datetime(2011, 10, 29, 20, 30, 21)
dt.year        # Python outputs 2011
dt.second      # Python outputs 21
dt.date()      # Python outputs 'datetime.date(2011,10,29)'
dt.time()      # Python outputs 'datetime.time(20,30,21)'
# The 'strftime' method formats a datetime as a string
dt.strftime('%m/%d/%Y %H:%M')   # Python outputs "30/29/2011 20:30"
# Strings can be parsed into datetime objects using the 'strptime' function:
datetime.strptime('20091031','%Y%m%d')  # Python outputs 'datetime.datetime(2009, 10, 31, 0, 0)'
datetime.strptime('20091031123014','%Y%m%d%H%M%S')   # Python outputs 'datetime.datetime(2009, 10, 31, 12, 30, 14)'
# You can replace fields of a series of datetimes, for example replacing the minute and second fields with zero, 
# thus producing a new object:
dt.replace(minute = 0, second = 0)    # Python outputs 'datetime.datetime(2011, 10, 29, 20, 0)'
# The difference between two datetime objects produces a datetime.timedelta type:
dt2 = datetime(2011,11,15,22,30)
delta = dt2 - dt
delta   # Python outputs 'datetime.timedelta(17, 7179)'
type(delta)    # Python outputs 'datetime.timedelta'
# You can also add delta back to datetime to produce a new shifted datetime

# No.12 Control Flow  
# 12.1 if, elif, and else
x = 10
if x < 0:
    print "It's negative"
elif x == 0:
    print 'Positive but smaller than 5'
else:
    print 'Positive and larger than or equal to 5'
# If any of the conditions is True, no further elif or else blocks will be reached. 

# With a compound condition using 'and' or 'or', conditions are evaluated left-to-right and will short circuit:
a = 5; b = 7
c = 8; d = 4
if a < b or c > d:
    print 'Made it'
# In this example, the comparison c > d never gets evaluated because the first comparison was True

# 12.2 For loops
# for loops are for iterating over a collection (like a list or tuple) or an iterater. 
# Using the 'continue' keyword, a for loop can be advanced to the next iteration, skipping the remainder of the block. For instance:
# This code sums up integers in a list and skips None values
sequence = [1,2,None,4,None,5]
total = 0
for value in sequence:
    if value is None:
        continue
    total += value         
total                          # Python outputs 12

# Using 'break' keyword, a for loop can be exited altogether. For instance:
# This code sums elements of a list until a 5 is reached:
sequence = [1,2,0,4,6,5,2,1]
total_until_5 = 0
for value in sequence:
    if value == 5:
        break
    total_until_5 += value
total_until_5                 # Python outputs 13
    
# 12.3 While loops
# A while loop specifies a condition and a block of code that is to be executed until the condition evaluates to False
# or the loop is explicitly ended with break. For instance:
x = 256
total = 0
while x > 0:
    if total > 500:
        break
    total += x
    x = x//2
total
    
# 12.4 Pass
# Pass can be used in blocks where no action is to be taken; it's common to use pass as a place-holder in code  
# while working on a new piece of functionality
if x < 0:
    print 'negative!'
elif x == 0:
    # ToDo: put something smart here
    pass
else:
    print 'positive!'

# 12.5 Exception handling
# Handling Python errors or exceptions gracefully is an important part of building robust programs. For instance, 
# Python's float function is able to cast a string to a floating point number, but fails with ValueError on improper inputs:
float('1.2345')      # Python outputs 1.2345
float('something')   # Python outputs ValueError: could not convert string to float: something
# Suppose we wanted a version of float that fails gracefully, returning the input argument. We can do this by writing a function
# that encloses the call to float in a try/except block:
def attempt_float(x):
    try:
        return float(x)
    except:
        return x
# The code in the except part of the block will only be executed if float(x) raises an exception:
attempt_float('1.2345')    # Python outputs 1.2345
attempt_float('something') # Python outputs 'something'

# Sometimes float function can raise exceptions other than ValueError. For instance:
float((1,2))       # Python outputs TypeError: float() argument must be a string or a number
# You might only want to suppress ValueError, since a TypeError (the input was not a string or numeric value) might indicate a legitimate bug
# in your program). To do that, write the exception type after except:
def attempt_float(x):
    try:
        return float(x)
    except ValueError:
        return x
attempt_float((1,2))   # Python outputs TypeError: float() argument must be a string or a number

# You can catch multiple exception types of writing a tuple of exception types instead (the PARENTHESES are required)
def attempt_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return x

# In some cases, you may not want to suppress an exception, but you want some code to be executed regardless of whether the code in the 'try' block
# succeeds or not. To do this, use 'finally':
f = open(path, 'w')
try: 
    write_to_file(f)
finally:
    f.close()
# Here the file handle f will always get closed. 
# Similarly, you can have code that executes only if the 'try' block succeeds using 'else':
f = open(path, 'w')
try: 
    write_to_file(f)
except:
    print 'Failed'
else:
    print 'Succeeded'
finally:
    f.close()

# 12.6 Range and xrange
# The range function produces a list of evenly-spaced integers:
range(10)       # Python outputs a list [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Both a start, end, and step can be given:
range(0, 20, 2)  # Python outputs a list [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
# As you can see, 'range' produces integers up to but not including the endpoint. 
# A common use of range is for iterating through sequences by index:
seq = [1, 2, 3, 4]
for i in range(len(seq)):
    val = seq[i]

# For very long ranges, it's recommended to use xrange, which takes the same arguments as range 
# but returns an iterator that generates integers one by one rather than generating all of them up-front 
# and storing them in a (potentially very large) list. For instance
# This code sums all numbers from 0 to 9999 that are multiples of 3 or 5:
sum = 0
for i in xrange(10000):
    if i % 3 == 0 or i % 5 == 0:
        sum += i
# Note: In Python 3, range always returns an iterator. Thus it's no longer necessary to use the xrange function

# 12.7 Ternary Expressions
# A ternary expression in Python allows you to combine an if-else block which produces a value into a single line or expression. For instance:
x = 5
'Non-negative' if x >= 0 else 'Negative'
# As with if-else blocks, only one of the expressions will be evaluated.
# While it may be tempting to always use ternary expressions to condense your code, note that you may sacrifice readability if 
# the true and false expressions are very complex

## Data Structures and Sequences

# No.1 Tuple
# A tuple is a one-dimensional, fixed-length, immutable sequence of Python objects. 
# Tuple can simply be created with a comma-separated sequence of values
a = 4,5,6
# When defining tuples in more complicated expressions, it's often necessary to enclose the values in parentheses. For instance, 
# creating a nested tuple
nested_tuple = (4,5,6),(7,8)
nested_tuple    # Python outputs '((4,5,6),(7,8))'
# Using 'tuple' function, any sequence or iterator can be converted to a tuple
tuple([4,0,2])       # Python outputs (4, 0, 2)
b = tuple('string')  # Python outputs ('s', 't', 'r', 'i', 'n', 'g')

# Elements can be accessed with square brackets [] as with most other sequence types. 
b[4]      # Python outputs 'n'
# While the objects stored in a tuple may be mutable themselves, once created it's not possible to modify which object is stored in each slot
tup = tuple(['foo', [1,2], 8, True])
tup[3] = False   # Python outputs "'tuple' object does not support item assignment"

# However, 
tup[1].append(3)    # Python outputs ('foo', [1, 2, 3], 8, True)
tup
# Tuple can be concatenated using the '+' operator to produce longer tuples:
(4, None, 'foo') + (6, 0) + ('bar',)   # Python outputs (4, None, 'foo', 6, 0, 'bar')
# Multiplying a tuple by an integer, as with lists, has the effect of concatenating together that many copies of the tuple
('foo', 'bar') * 4    # Python outputs ('foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'bar')
# Note that only the reference to objects are copied, not objects themselves. 

# Unpacking tuples
# If you try to assign to a tuple-like expression of variables, Python will attempt to unpack the value on the right-hand side of the equal sign:
tup = (4,5,6)
a,b,c = tup
c     # Python outputs 6
# Even nested tuples can be unpacked:
tup = 4, 5, (6, 7)
a, b, c, d = tup
d    # Python outputs 7
# One of the most common use of variable unpacking when iterating over sequences of tuples or lists:
seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
for a,b,c in seq:
    pass
    
# Tuple methods
# Since the size and contents of a tuple cannot be modified, it is pretty light on instance methods. One particularly useful one (also available on list)
# is 'count', which counts the number of occurrences of a value:
a = (1, 2, 2, 2, 3, 4, 2)
a.count(2)    # Python outputs 4

# No.2 List
# Unlike tuples, lists are variable-length and their contents can be modified. They can be defined using square brackets [] or using the list type function:
a_list = [2, 3, 7, None]
tup = 'foo', 'bar', 'baz'
b_list = list(tup)
b_list.append('dwarf')    # Note: 'append' method treats the argument as one single object, no matter if the argument is a list or just a string
b_list       # Python outputs '['foo', 'bar', 'baz', 'dwarf']'

# Using 'insert' you can insert an element at a specific index in the list:
b_list.insert (1, 'red')
b_list      # Python outputs '['foo', 'red', 'bar', 'baz', 'dwarf']'

# Using 'pop' you can remove an element at a particular index:
b_list.pop(2)    # Python outputs "'bar'"
b_list           # Python outputs '['foo', 'red', 'baz', 'dwarf']'

# Elements can be removed by value using 'remove', which locates the first such value and removes it from the list:
b_list.append('foo')
b_list           # Python outputs '['foo', 'red', 'baz', 'dwarf', 'foo']'
b_list.remove('foo')
b_list           # Python outputs '['red', 'baz', 'dwarf', 'foo']'

# You can check if a list contains a value using the 'in' keyword:
'dwarf' in b_list   # Python prints True
# Note that checking whether a list contains a value is a lot slower than dicts and sets as Python makes a linear scan across the values of the list,
# whereas the others (based on hash tables) can make the check in constant time.

# Concatenating and combining lists
# 1st way: using '+' to concatenate two lists
[4, None, 'foo'] + [7, 8, (2, 3)]   # Python outputs '[4, None, 'foo', 7, 8, (2, 3)]'

# 2nd way: using 'extend' method to append a list to existing list
x = [4, None, 'foo']
x.extend([7, 8, (2, 3)])     # Note: unlike 'append' method, 'extend' method treats the argument as an extension of the existing list
x

# Note: Using 'extend' is preferable when building up a large list because everytime '+' is used a new list must be created and the objects copied over

# Sorting
# A list can be sorted in-place (without creating a new object) by calling its 'sort' method:
a = [7, 5, 1, 8, 3]
a.sort()
a
# You can also pass a secondary sort key i.e. a function that produces a value to use to sort the objects
# For instance, we could sort a collections of strings by their length:
b = ['saw', 'small', 'He', 'foxes', 'six']
b.sort(key = len)
b

# Binary Search
# The built-in 'bisect' module implements binary-search and insertion into a sorted list. 
# 'bisect.bisect' finds the location where an element should be inserted to
# while 'bisect.insort' actually inserts the element into that location:
import bisect
c = [1, 2, 2, 2, 3, 4, 7]
bisect.bisect(c, 2)         # Python outputs 4
bisect.bisect(c, 8)         # Python outputs 7

bisect.insort(c, 6)         
c                           # Python outputs [1, 2, 2, 2, 3, 4, 6, 7]

# Note: The 'bisect' module do not check whether the list is sorted. Thus using them with an unsorted list will succeed without error 
# but may lead to incorrect results

# Slicing 
# You can select sections of list-like types (arrays, tuples, NumPy arrays) by using slicing notation, which in its basic form consists of
# start:stop passed to the indexing operator []:
seq = [7, 2, 3, 7, 5, 6, 0, 1]
seq[1:5]            # Python outputs [2, 3, 7, 5]

# slices can also be assigned to with a sequence
seq[3:4] = [6, 3]
seq                 # Python outputs [7, 2, 3, 6, 3, 5, 6, 0, 1]

# Note: While element at the start index is included, the stop index is not included, so that the number of elements in the result is 
# stop - start

# Either the start or stop can be ommitted in which case they default to the start of the sequence and the end of the sequence:
seq[:4]         # Python outputs [7, 2, 3, 6]
seq[3:]         # Python outputs [6, 3, 5, 6, 0, 1]

# Negative indices slice the sequence relative to the end:
seq[-4:]       # Python outputs [5, 6, 0, 1]
seq[-6:-2]     # Python outputs [6, 3, 5, 6]

# A step can also be used after a second colon to take every other element
seq[::2]       # Python outputs [7, 3, 3, 6, 1]
# Passing -1 has the useful effect of reversing a list or tuple
seq[::-1]      # Python outputs [1, 0, 6, 5, 3, 6, 3, 2, 7]

## Built-in Sequence Functions
# 1. Enumerate
# Enumerate keeps track of the index of the current item. Python has a built-in function 'enumerate' which returns a sequence of (i, value) tuples
some_list = ['A', 'B', 'C']
mapping = dict((v, i) for i, v in enumerate(some_list))
mapping        # Python outputs {'A': 0, 'B': 1, 'C': 2}

some_list = ['foo', 'bar', 'caz']
mapping = dict((v, i) for i, v in enumerate(some_list))
mapping        # Python outputs {'bar': 1, 'caz': 2, 'foo': 0}

# 2. Sorted
# The sorted method returns a new sorted list from the elements of any sequence
sorted([7, 1, 2, 6, 0, 3, 2])    # Python outputs [0, 1, 2, 2, 3, 6, 7]

sorted('horse race')             # Python outputs [' ', 'a', 'c', 'e', 'e', 'h', 'o', 'r', 'r', 's']

# A common pattern for getting a sorted list of unique elements in a sequence is to combine sorted with set:
sorted(set('this is just some string'))

# 3. Zip
# zip "pairs" up the elements of a number of lists, tuples, or other sequences, to create a list of tuples:
seq1 = ['foo', 'bar', 'baz']
seq2 = ['one', 'two', 'three']
zip(seq1, seq2)        # Python outputs [('foo', 'one'), ('bar', 'two'), ('baz', 'three')]

# Zip can take an arbitrary number of sequences, and the number of elements it produces is determiend by the shortest sequence:
seq3 = [False, True]
zip(seq1, seq2, seq3)  # Python outputs [('foo', 'one', False), ('bar', 'two', True)]

# A very common use of zip is for simultaneously iterating voer multile sequences, possibly also combined with 'enumerate'
for i, (a, b) in enumerate(zip(seq1, seq2)):
    print ('%d: %s, %s' %(i, a, b))   # Python outputs 0: foo, one
                                       #                1: bar, two
                                       #                2: baz, three
                            
# Given a "zipped" sequence, zip method can be applied in a way to "unzip" the sequence, i.e. converting a list of rows into a list of columns.
pitchers = [('Nolan', 'Ryan'), ('Roger', 'Clemens'), ('Schilling', 'Curt')]
first_names, last_names = zip(*pitchers)
first_names         # Python outputs ('Nolan', 'Roger', 'Schilling')
last_names          # Python outputs ('Ryan', 'Clemens', 'Curt')

# 4. reversed 
# reverse iterates over the elements of a sequence in reverse order:
list(reversed(range(10)))    # Python outputs [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# No.3 Dict
# Dict is a very important built-in Python data structure. A more common name for it is hash map or associative array. 
# It is a flexibly-sized collection of key-value pairs, where key and value are Python objects. 
d1 = {'a':'some value', 'b': [1, 2, 3, 4]}
d1

# Elements can be accessed and inserted using the same syntax as accessing elements of a list or tuple:
d1[7] = 'an integer'   
d1                 # Python outputs {7: 'an integer', 'a': 'some value', 'b': [1, 2, 3, 4]}
d1['b']            # Python outputs [1, 2, 3, 4]

# You can check if a dict contains a key using the same syntax as with checking whether a list or tuple contains a value:
'c' in d1          # Python outputs False
'a' in d1          # Python outputs True

# Values can be deleted either using the 'del' keyword or the 'pop' method (which simultaneously returns the value and deletes the key):
d1[5] = 'some value'
d1
d1['dummy'] = 'another value'
del d1[5]
d1
d1.pop('dummy')     # Python outputs 'another value'
d1

# The 'keys' and 'values' method give you lists of the keys and values, respectively. While the key-value pairs are not in any particular order, 
# these functions output the keys and values in the same order:
d1.keys()          # Python outputs ['a', 'b', 7] 
d1.values()        # Python outputs ['some value', [1, 2, 3, 4], 'an integer']
# Note: if you use Python 3, dict.keys() and dict.values() are iterators instead of lists

# Use 'update' method to merge one dict into another 
d1.update({'b': 'foo', 'c': 12})

# You can get a bit creative with 'zip' method in dict
key_list = ['Bob', 'Adam', 'Cathy']
value_list = [15, 22, 8]
mapping = {}
for key, value in zip(key_list, value_list):
    mapping[key] = value
mapping           # Python outputs {'Adam': 22, 'Bob': 15, 'Cathy': 8}

# dict type function accepts a list of 2-tuples
mapping = dict(zip(range(5), reversed(range(5))))
mapping       # Python outputs {0: 4, 1: 3, 2: 2, 3: 1, 4: 0}

# Default values?

# Valid dict key types
# While the values of a dict can be any Python object, the keys have to be IMMUTABLE objects like scalar types (int, float, string)
# or tuples (all the objects in the tuple need to be immutable, too). In other words, you want to check whether an object is hashable
# (can be used as a key in a dict) with the hash function:
hash(100)     # Python outputs 100
hash('Spring')  # Python outputs -1201250839
hash((1,2,(2,3))) # Python outputs 1387206534
hash((1,2,[2,3])) # Python outputs TypeError: unhashable type: 'list'
