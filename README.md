# Course Scheduling

## Initial Plan
In my initial plan, I illustrated my main idea of the course scheduling project,
described the Coffman-graham algorithm that I will be working on, and some difficulties as well as interesting points.
[research-initial-plan.pdf](research-initial-plan.pdf)

## TODOs
1. some courses are also GEs, should not take GEs again.(need so much more infomation, may avoid doing this part to better research algorithms)
2. refactor code.

## Current Results
1. solve the problem that some courses are upper division student only.

    - method 1: adding another queue: this still cannot solve the problem that some courses will be added to a lower division level. May solve later after refactor the scheduling code. 
    
    - method 2: pushing this course back into the end of the queue. This somewhat guarantees that this course will not show up too early until some other courses that are not upper division students only are assigned. However, if there are so many courses like GE in the queue, then it will deplay the process. (Having GEs when scheduling will result in a worse schedule)

2. it can pick more courses randomly to fullfill the 11 upper requirement after loading 11 upper requirement in the specialization txt file. 

3. A Simple Schedule

    This schedule takes GE requirement, specialization requirement, the quarter offering and course units into account.
     It adds GE requirement later after major requirement courses are assigned. (on average this can get a better result than adding them together)

    **sample:**
    ```
    Taking 16 credits per quarter:
    year 1 quarter 1: ['I&CSCI90', 'I&CSCI31', 'I&CSCI6B', 'MATH2A']
    year 1 quarter 2: ['IN4MATX131', 'I&CSCI32', 'I&CSCI6D', 'MATH2B']
    year 1 quarter 3: ['I&CSCI51', 'I&CSCI33', 'IN4MATX43']
    year 2 quarter 1: ['MATH3A', 'STATS67', 'COMPSCI151', 'I&CSCI45C']
    year 2 quarter 2: ['COMPSCI122A', 'IN4MATX113', 'COMPSCI178', 'COMPSCI152']
    year 2 quarter 3: ['COMPSCI132', 'COMPSCI154', 'I&CSCI46', 'GEIV-3']
    year 3 quarter 1: ['COMPSCI184A', 'COMPSCI169', 'IN4MATX115', 'COMPSCI171']
    year 3 quarter 2: ['COMPSCI133', 'COMPSCI161', 'COMPSCI116', 'COMPSCI175']
    year 3 quarter 3: ['GEVIII-1', 'GEIV-2', 'GEVII-1', 'GEVI-1']
    year 4 quarter 1: ['GEII-1', 'GEIV-1', 'GEII-2']
    ```

4. Original coffman-graham algorithm.
    - [directedGraphRepresentation](coffman_graham_algorithm/directedGraphRepresentation.py)
    - [coffman-graham algorithm](coffman_graham_algorithm/coffman-grapham.py)

5. Crawler
    - [WebSoc and prerequistes Crawler (using beautiful soup and requests libraries)](WebSoc.py)

    - Right now it still cannot get those courses without prereqs automatically

6. Courses information I got from [www.reg.uci.edu](https://www.reg.uci.edu/cob/prrqcgi?term=201703&dept=COMPSCI&action=view_by_term#115) and [WebSoc](https://www.reg.uci.edu/perl/WebSoc). I integrated my crawlers into one on week 4 in Winter quarter.

    **sample**:
    - [WRITING, I&C SCI, COMPSCI Depts data](info/test/fullcourses.txt)

    In the txt file, each line contains info of a course and the line is separated by ";". Line is in the following format:
    ```[department code];[course num];[title];[prereqs];[units];[quarters]```
    e.g.
    ```I&CSCI;6D;DISCRET MATH FOR CS;[{'I&CSCI6B'}];4;{0, 1, 2}```

7. CS specializations information I got manually from [catalogue.uci.edu](http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext)

    **sample**:
    - [CS specializations](info/specializations.txt)




## Schedule

### 2017 Winter Quarter
During winter quarter, I will implement the algorithm and resolve dificulties described. I
will also have a working application done by the end of this quarter.
- **Week 1:** (Done) Find a method to represent the study plan graph.

- **Week 2:** (Done) Apply the basic Coffman-Graham algorithm, which defines a fixed width bound $ W $, and test its performance in this particular course scheduling problem assuming that the number of classes a student takes will not exceed a fixed width bound.

- **week 3:** (Done) Collect courses information online by using web crawlers.

- **Week 4, 5, 6:** (In progress) Modify the algorithm to solve difficulties illustrated and test the quality of the final algorithm.

- **week 7, 8, 9, 10:** Find other similar algorithms and compare them with coffman-graham algorithm. 

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