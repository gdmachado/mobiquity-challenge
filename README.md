# Mobiquity Challenge

This is my proposed solution for the challenge sent to me during the application process for a Data Engineer position within Mobiquity.

## Usage

Make sure you have Python 3.x installed. The pack.py file is executable, and looks for `python3` in `/usr/bin/env`.

Also, for running the tests suite, you need `pytest` installed:

    $ pip3 install -U pytest

### Running tests suite

    $ py.test -v

### Running solution over input_file

    $ ./pack.py input_filename

## My proposed solution

This is a classic example of the [0-1 Knapsack Problem](https://en.wikipedia.org/wiki/Knapsack_problem), which is a NP-Hard problem (the optimization part). I will assume that this could scale, and try to implement the algorithm as efficiently as possible.

We will use a [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) approach for solving this problem. This way we can avoid recursion (and memory issues when the problem is big enough), and will solve the problem in pseudo-polynomial time.

For the problem to be solved using Dynamic Programming, all weights need to be a non-negative integer, so we will multiply all weights by 100.

I have altered a detail from one of the original constraints for structural's sake. Basically, the `pack` method  inside my `Packer` class will not accept the absolute path for the input file (as originally requested), but instead will expect a tuple containing all details about the package in question and it's things. The logic for looping through all of the input's files and parsing each row will be done outside of the class, within the `main` method.

Also, the solution is implemented and expects to be ran in Python 3.

## The challenge

### Introduction

You want to send your friend a package with different things.

Each thing you put inside the package has such parameters as index number, weight and cost. The package has a weight limit. Your goal is to determine which things to put into the package so that the total weight is less than or equal to the package limit and the total cost is as large as possible.

You would prefer to send a package which weights less in case there is more than one package with the same price.

### Input Sample

Your program should accept as its first argument a path to a filename. The input file contains several lines. Each line is one test case.

Each line contains the weight that the package can take (before the colon) and the list of things you need to choose. Each thing is enclosed in parentheses where the 1st number is a thing's index number, the 2nd is its weight and the 3rd is its cost. E.g.

    81 : (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) (5,30.18,€9)
    (6,46.34,€48)
    8 : (1,15.3,€34)
    75 : (1,85.31,€29) (2,14.55,€74) (3,3.98,€16) (4,26.24,€55) (5,63.69,€52)
    (6,76.25,€75) (7,60.02,€74) (8,93.18,€35) (9,89.95,€78)
    56 : (1,90.72,€13) (2,33.80,€40) (3,43.15,€10) (4,37.97,€16) (5,46.81,€36)
    (6,48.77,€79) (7,81.80,€45) (8,19.36,€79) (9,6.76,€64)

### Output sample

For each set of things that you put into the package provide a list (items’ index numbers are separated by comma). E.g.

    4
    -
    2,7
    8,9

### Constraints

You should write a class `com.mobiquityinc.packer.Packer` with a static method named pack. This method accepts the absolute path to a test file as a String. It does return the solution as a String.

Your class should throw an `com.mobiquityinc.exception.APIException` if incorrect parameters are being passed.

Additional constraints:

1. Max weight that a package can take is ≤ 100
2. There might be up to 15 items you need to choose from
3. Max weight and cost of an item is ≤ 100

### Remember

Apply best practices for software design & development and document your approach (what strategy/algorithm/data structure/design pattern you chose and why) and put comments into your source files.

### Your Result

When finished, please send a zip file that includes the java source files to your contact person within Mobiquity. The source code will be examined by one of our developers.
Good luck with this assignment. If you have any questions, don’t hesitate to ask your contact person within Mobiquity.
