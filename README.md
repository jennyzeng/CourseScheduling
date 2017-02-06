# Course Scheduling

## Initial Plan
In my initial plan, I illustrated my main idea of the course scheduling project,
described the Coffman-graham algorithm that I will be working on, and some difficulties as well as interesting points.
[research-initial-plan.pdf](research-initial-plan.pdf)

## TODOs
1. solve the problem that some courses are upper division student only
2. it should pick more courses randomly to fullfill the 11 upper requirement
3. some courses are also GEs, should not take GEs again.
4. load data into database
5. refactor code.

## Current Results
1. Original coffman-graham algorithm.
    - [directedGraphRepresentation](coffman_graham_algorithm/directedGraphRepresentation.py)
    - [coffman-graham algorithm](coffman_graham_algorithm/coffman-grapham.py)

2. Crawler
    - [WebSoc and prerequistes Crawler (using beautiful soup and requests libraries)](WebSoc.py)

    - Right now it still cannot get those courses without prereqs automatically

3. Courses information I got from [www.reg.uci.edu](https://www.reg.uci.edu/cob/prrqcgi?term=201703&dept=COMPSCI&action=view_by_term#115) and [WebSoc](https://www.reg.uci.edu/perl/WebSoc). I integrated my crawlers into one on week 4 in Winter quarter.

    **sample**:
    - [WRITING, I&C SCI, COMPSCI Depts data](info/test/fullcourses.txt)

    In the txt file, each line contains info of a course and the line is separated by ";". Line is in the following format:
    [department code];[course num];[title];[prereqs];[units];[quarters]
    e.g.
    I&CSCI;6D;DISCRET MATH FOR CS;[{'I&CSCI6B'}];4;{0, 1, 2}

4. CS specializations information I got manually from [catalogue.uci.edu](http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext)

    **sample**:
    - [CS specializations](info/specializations.txt)


4. A Simple Schedule

    This schedule takes GE requirement, specialization requirement, the quarter offering and course units into account. It adds GE requirement later after major requirement courses are assigned.

    **sample:**
    ```
    Taking 16 credits per quarter:
    year 1 quarter 1: ['I&CSCI6B', 'I&CSCI31', 'MATH2A', 'I&CSCI90']
    year 1 quarter 2: ['I&CSCI6D', 'COMPSCI125', 'I&CSCI51']
    year 1 quarter 3: ['I&CSCI32', 'MATH2B', 'GEVII-1', 'GEVb']
    year 2 quarter 1: ['IN4MATX43', 'I&CSCI33', 'STATS67', 'MATH3A']
    year 2 quarter 2: ['I&CSCI45C', 'COMPSCI178', 'GEVIII-1', 'GEII-2']
    year 2 quarter 3: ['I&CSCI46', 'GEIV-2', 'GEIV-3', 'GEII-1']
    year 3 quarter 1: ['COMPSCI169', 'COMPSCI171', 'COMPSCI161', 'GEII-3']
    year 3 quarter 2: ['COMPSCI175', 'GEIV-1', 'GEVa', 'GEVI-1']
    ```

## Schedule

### 2017 Winter Quarter
During winter quarter, I will implement the algorithm and resolve dificulties described. I
will also have a working application done by the end of this quarter.
- **Week 1:** (Done) Find a method to represent the study plan graph.

- **Week 2:** (Done) Apply the basic Coffman-Graham algorithm, which defines a fixed width bound $ W $, and test its performance in this particular course scheduling problem assuming that the number of classes a student takes will not exceed a fixed width bound.

- **week 3:** (Done) Collect courses information online by using web crawlers.

- **Week 4, 5, 6:** (In progress) Modify the algorithm to solve difficulties illustrated and test the quality of the final algorithm.

- **week 7, 8, 9, 10:** Implement the algorithm by using collected data. May make a simple working command-line interface first, and if time permits, develop a web-based application.

### 2017 Spring Quarter

During spring quarter, I will focus on writing and revising the project report. 

- **Week 1:** An outline of the project report.

- **Week 2:** First 1/3 of the project report.

- **Week 3:** Second 1/3 of the project report.

- **Week 4:** Third 1/3 of the project report.

- **Week 5, 6:** Second draft of the project report.

- **Week 7, 8:** Third draft of the project report.

- **Week 9:**  Forth draft of the project report. 

- **Week 10:** Final draft of the project report. 