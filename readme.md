# Response to a Software Design Challenge #

Extract from James Shore's [Architectural Design Challenge](http://www.jamesshore.com/Blog/Architectural-Design-Challenge.html)

***
***

## The Challenge ##

Write a command-line program that loads a file into memory, ROT-13s it, displays the result on the screen, and writes the result to a file.

***
***

## The Rules ##

### Part 1 ###

Test Design:
  - All code is tested.
  - The test code is as high-quality as the production code.
  - All business logic code (that is, the ROT13 code) is tested with unit tests that don't do any I/O.
  - All integration code (that is, the file and console I/O) is tested with focused integration tests that validate that the I/O libraries each work as expected, independently of the rest of the system.
  - End-to-end integration tests (that is, tests that check the system as a whole) are kept to a minimum, or better still, entirely unneeded.

Coupling and Cohesion:
  - The code reflects the usage and the external behavior of the system more than it reflects the techniques used in coding, so that any concept (such as "loads and saves files" or "rot13") can be clearly related to specific code.
  - Code related to a single concept is grouped together.
  - Code for unrelated concepts (such as "rot13" and "file handling") is stored in separate locations.

Simplicity:
  - Classes' public interfaces are clear and easy to understand.
  - Individual lines of code read well.
  - Boilerplate code is kept to a minimum.
  - Lines of code are kept to a minimum.
  - There is no code that anticipates part two of the challenge.

Quality Without a Name:
  - The code feels beautiful and well designed.
  - The system follows the spirit of the rules: it illustrates a general architectural approach, not a problem-specific hack.

### Part 2 ###

Mutability:
  - A minimum number of lines of code needed to be changed.
  - A minimum--preferably zero--of the code not related to file-handling needed to be changed.
  - Most--preferably all--of the file-handling changes were in a single place.


***
***

## Usage ##

### Example ###
```sh
$ echo 'Caeser Cipher' | tr 'A-MN-Za-mn-z' 'N-ZA-Mn-za-m' > in.txt
$ cat in.txt
Pnrfne Pvcure
$ python r.py -i in.txt -o out.txt
$ cat out.txt
Caesar Cipher
```

### Test ###
```sh
$ nosetests r.py
............
----------------------------------------------------------------------
Ran 12 tests in 0.188s

OK
```
