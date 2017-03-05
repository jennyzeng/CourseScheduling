# Course Scheduling

## Initial Plan
In my initial plan, I illustrated my main idea of the course scheduling project,
described the Coffman-graham algorithm that I will be working on, and some difficulties as well as interesting points.
[research-initial-plan.pdf](research-initial-plan.pdf)

## TODOs
1. Evaulate the quality of solution
2. Compare it with other job scheduling algorithms

## How to use this algorithm right now

1. download the whole repo
2. Install Python3
3. If use taken (allow user to start from the mid way): create a txt file called "taken.txt" in the root directory, and input your info in the following format:
    1. first line: next quarter code. 0: Fall, 1: Winter, 2: Spring
    2. second line: credits applied
    3. for every line after the first two line, open UCI student access, input courses that you have already taken, and can satisfy your requirement.
    if it is a GE course and does not satisfy any major requirement, put GE[category] -1,GE[category] -2,GE[category] -3 in it. No repetitions, and the number followed by the GE name is in range [1,3].
    sample: [taken.txt](info/test/taken.txt)

4. If use avoid (allow user to avoid taking some courses): create a txt file called "avoid.txt" in the root directory and input courses you want to avoid.

5. In [main.py](main.py), edit the path for taken.txt. If you don't want to use taken, set useTaken=False
7. run main.py and you will get a schedule.

NOTE: Currently it only has information for CS major with specific specializations. Not for students with other majors or at other schools.


## Current Course Scheduling Algorithm
### in main:
```
Load specialization info into SpecsTable
load course infomation into graphs
For each course in graph:
    update the course dependent info
    update course specialization satisfaction info
Start to do multigraph scheduling
```


### in Scheduling algorithm

- L: is the scheduling output, which is initially ```[[]]``` before doing
scheduling for all the graphs.

- Q: store the courses that are going to be scheduled into L. prereqs of all courses in the queue are already satisfied.

- define number of courses in graph to be n.

- define the number of levels in L to be m. 0<m<n

- define the maximum width of a level to be w.  0<w<n and w = n/m

```
INPUT:
    - L: current schedule
    - graph: a course graph
    - specsTable: store specs that should be satisfied
    - upperBound: above what levels a upper standing course can be assgined

OUTPUT: L

initialize Q, maxheap structure, and add courses without prereqs into it

while Q is not empty:                                                           # O(n) times
    currentCourse = Q.pop()         # O(1)

    discard currentCourse if it does not satisfy any specializations

    if the highest level has dependents, it has to be assigned to a new level.
        Then assigned = True
    else: assigned = False

    if not assigned:       # the highest level does not have cur's dependents
        step = the second highest level index
        if the highest level is full, we have to create a new level
            and then create more levels until it find the nearest quarter that
            this course is offered.                                             # O(w)
        lastStep = the highest level index (lowest acceptable one so far)

        while not assigned to the schedule and step >= 0: # O(m) times

            if there are dependents in level L[step]:           # O(w)
                it cannot be assigned to a higher level,
                 we assign it to the level L[lastStep]
                 assigned = True

            else:
                if course is upper standing only and step < upperBound:
                    assign it to the level L[lastStep]
                    assigned = True

                else if this level is not full,
                    and currentCourse will be offered this quarter,
                    then this is a possible level for this course.  # O(w)
                    we will mark:
                        lastStep = step
            step--

        if the course is still not assigned after looking over all levels in schedule:
            course will be assigned to the lowest acceptable level L[lastStep]

        we are sure that the course is assigned, then we will add those courses
            that will be satisfied after assigning this course into Q           # O(nlogn)

        add currentCourse units into the total units assigned       # O(1)

    clear empty levels at the end of L
    return L
```

- creating new levels until find the nearest quarter that this course is offered is
O(1) because it will create at most 3 levels for a course
- any pop or push operation is O(1)
- the first while loop will loop through O(n) times
- between first while loop and the third one: O(n+2w) = O(n+w)=O(n)
- third while loop: O(m) times
- in third while loop: O(2w) = O(w)
- lastly, push at most n elements into a max heap is O(nlogn)
- total is O(n)\*(O(n)+O(m)\*O(w) + O(nlogn)) = O(n)\*O(nlogn) = O(n^2logn)



## Current Results

1. Implement Hu's Algorithm by labeling each course with a distance.

    - distance calculation: its own course value + distance to the "sink"

    - course value calculation: the number of specializations it satisfies.

    After labeling, when a user takes 20 credits per quarter, the user can fulfill requirements in 3 years.
    On the contrary, without labeling, it takes the user 3 years and 1 quarter.

2. Allow input what courses the user want to avoid.

3. Allow input courses already taken and schedule from the half-way.

4. Max heap with a heuristic estimation for course values for better performance, but increase the time complexity

5. It will make schedules on a upper bound range and pick the most efficient one.

6. solve the problem that some courses are upper standing student only.
    Set a upper bound advanced. The bound will prevent the algorithm from assigning upper standing only courses into a level < upper bound (specified in function).

7. it can pick more courses randomly to fullfill the 11 upper requirement after loading 11 upper requirement in the specialization txt file.

8. A Simple Schedule

    This schedule can handle the following conditions:

    1. GE requirement
    2. specialization requirement
    3. the quarter offering and course units
    4. Some courses are upper division standing only

    **sample:**
    - CS Student specialized in Intelligent Systems and Algorithms. No taken.
        ```
        start quarter:  0
        Taking 20 credits per quarter:
        year 1 quarter 1: ['I&CSCI31', 'MATH2A', 'I&CSCI6B', 'WRITINGLOW1', 'HISTORY40A']
        year 1 quarter 2: ['I&CSCI32', 'MATH2B', 'I&CSCI6D', 'I&CSCI51']
        year 1 quarter 3: ['I&CSCI33', 'STATS67', 'MATH3A', 'HISTORY40C', 'POLSCI21A']
        year 2 quarter 1: ['I&CSCI45C', 'COMPSCI151', 'COMPSCI169', 'GEII-1', 'GEIII-1']
        year 2 quarter 2: ['I&CSCI46', 'COMPSCI178', 'COMPSCI121', 'HISTORY40B', 'GEIII-2']
        year 2 quarter 3: ['COMPSCI177', 'GEVI-1', 'GEVII-1', 'GEVIII-1', 'IN4MATX43']
        year 3 quarter 1: ['COMPSCI161', 'COMPSCI171', 'I&CSCI90', 'WRITINGLOW2']
        year 3 quarter 2: ['COMPSCI162', 'COMPSCI116', 'COMPSCI175', 'I&CSCI53+53L']
        year 3 quarter 3: ['COMPSCI163', 'COMPSCI165', 'I&CSCI139W']
        best upper bound: year 2 quarter 3
        ```

    - CS Student specialized in Intelligent Systems and Algorithms. Use "taken".
        ```
        start quarter:  2
        Taking 20 credits per quarter:
        year 1 quarter 3: ['COMPSCI177', 'COMPSCI163', 'COMPSCI165', 'COMPSCI175', 'GEVII-1']
        year 2 quarter 1: ['COMPSCI151', 'COMPSCI169', 'HISTORY40A', 'I&CSCI139W']
        year 2 quarter 2: ['COMPSCI167', 'HISTORY40B', 'I&CSCI53+53L']
        best upper bound: year 1 quarter 1
        ```

    - CS Student specialized in Intelligent Systems and Algorithms. Use "taken" and "avoid" ( we see that it avoids taking COMPSCI151 so it takes COMPSCI111 instead)
        ```
        start quarter:  2
        Taking 20 credits per quarter:
        year 1 quarter 3: ['COMPSCI177', 'COMPSCI163', 'COMPSCI165', 'COMPSCI175', 'GEVII-1']
        year 2 quarter 1: ['COMPSCI169', 'HISTORY40A', 'COMPSCI111', 'I&CSCI139W']
        year 2 quarter 2: ['COMPSCI167', 'HISTORY40B', 'I&CSCI53+53L']
        best upper bound: year 1 quarter 1
        ```

9. Original coffman-graham algorithm.
    - [directedGraphRepresentation](coffman_graham_algorithm/directedGraphRepresentation.py)
    - [coffman-graham algorithm](coffman_graham_algorithm/coffman-grapham.py)

10. Crawler
    - [WebSoc and prerequistes Crawler (using beautiful soup and requests libraries)](WebSoc.py)

    - Right now it still cannot get those courses without prereqs automatically
    - For courses such as I&CSCI 51, have to manually modify it to be I&CSCI 51+51L, and change the units to be 6.

11. Courses information I got from [www.reg.uci.edu](https://www.reg.uci.edu/cob/prrqcgi?term=201703&dept=COMPSCI&action=view_by_term#115) and [WebSoc](https://www.reg.uci.edu/perl/WebSoc). I integrated my crawlers into one on week 4 in Winter quarter.

    **sample**:
    - [Courses info in some departments](info/test/fullcourses.txt)

    In the txt file, each line contains info of a course and the line is separated by ";". Line is in the following format:
    ```[department code];[course num];[title];[prereqs];[units];[quarters];[isUpperOnly]```
    e.g.
    ```I&CSCI;6D;DISCRET MATH FOR CS;[{'I&CSCI6B'}];4;{0, 1, 2};False```


    NOTE: Courses information here is just used for testing and is not accurate because the quarters a course will be offered may vary each year.


12. CS specializations information I got manually from [catalogue.uci.edu](http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext)

    **sample**:
    - [CS specializations](info/test/specializations.txt)


## Research Project Schedule

### 2017 Winter Quarter
During winter quarter, I will implement the algorithm and resolve dificulties described. I
will also have a working application done by the end of this quarter.
- **Week 1:** (Done) Find a method to represent the study plan graph.

- **Week 2:** (Done) Apply the basic Coffman-Graham algorithm, which defines a fixed width bound $ W $, and test its performance in this particular course scheduling problem assuming that the number of classes a student takes will not exceed a fixed width bound.

- **week 3:** (Done) Collect courses information online by using web crawlers.

- **Week 4, 5, 6:** (Done) Modify the algorithm to solve difficulties illustrated and test the quality of the final algorithm.

- **Week 7, 8:** (Done) Research on and implement the Hu's Algorithm.

- **Week 9, 10:** (In progress) Find other similar algorithms and compare them with coffman-graham algorithm.

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