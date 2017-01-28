# Course Scheduling

## Initial Plan
In my initial plan, I illustrated my main idea of the course scheduling project,
described the Coffman-graham algorithm that I will be working on, and some difficulties as well as interesting points.
[research-initial-plan.pdf](research-initial-plan.pdf)

## Current Results

1. some courses prerequisite infomation I got from [www.reg.uci.edu](https://www.reg.uci.edu/cob/prrqcgi?term=201703&dept=COMPSCI&action=view_by_term#115). I am still working on improving the code of my crawlers.
**samples**:
    - [COMPSCI prereqs](info/COMPSCI.txt)
    - [I&CSCI prereqs](info/I&SCI.txt)
    - [IN4MATX prereqs](info/IN4MATX.txt)
    - [STATS prereqs](info/STATS.txt)
    - [WRITING prereqs](info/WRITING.txt)
    - [MATH prereqs](info/MATH.txt)

    In the txt file, each line contains info of a course and the line is separated by ";". First part is course code (e.g. COMPSCI111), second part is course name (e.g. DIGITAL IMAGE PROC), and the third part is its prereqs. Prereqs are in the format of a list of sets to represent the AND/OR relationship.


## Schedule

### 2017 Winter Quarter
During winter quarter, I will implement the algorithm and resolve dificulties described. I
will also have a working application done by the end of this quarter.
- **Week 1:** (Done) Find a method to represent the study plan graph.

- **Week 2:** (Done) Apply the basic Coffman-Graham algorithm, which defines a fixed width bound $ W $, and test its performance in this particular course scheduling problem assuming that the number of classes a student takes will not exceed a fixed width bound.

- **week 3:**(in progress) Collect courses information online by using web crawlers or a UCI-Course-API on GitHub.

- **Week 4, 5, 6:** Modify the algorithm to solve difficulties illustrated and test the quality of the final algorithm.

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