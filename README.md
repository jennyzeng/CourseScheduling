# Course Scheduling

## Initial Plan
In my initial plan, I illustrated my main idea of the course scheduling project,
described the Coffman-graham algorithm that I will be working on, and some difficulties as well as interesting points.
[research-initial-plan.pdf](research-initial-plan.pdf)

## Current Results
1. Original coffman-graham algorithm.
    - [directedGraphRepresentation](coffman_graham_algorithm/directedGraphRepresentation.py)
    - [coffman-graham algorithm](coffman_graham_algorithm/coffman-grapham.py)

2. Crawlers
    - [Course Prerequisites Crawler (using Scrapy framework)](courseCrawler/courseCrawler/spiders/csCourseSpider.py)
    - [WebSoc Crawler (using beautiful soup and requests libraries)](WebSoc.py)

3. some courses infomation I got from [www.reg.uci.edu](https://www.reg.uci.edu/cob/prrqcgi?term=201703&dept=COMPSCI&action=view_by_term#115) and [WebSoc](https://www.reg.uci.edu/perl/WebSoc). I am still working on improving the code of my crawlers.

    **samples**:
    - [COMPSCI](info/COMPSCI.txt)
    - [I&CSCI](info/I&SCI.txt)
    - [IN4MATX](info/IN4MATX.txt)
    - [STATS](info/STATS.txt)
    - [WRITING](info/WRITING.txt)
    - [MATH](info/MATH.txt)
    - [test data1](info/test/courses.txt)
    - [test data2](info/test/courses2.txt)

    In the txt file, each line contains info of a course and the line is separated by ";". Line is in the following format: First part is course code (e.g. COMPSCI111); second part is course name (e.g. DIGITAL IMAGE PROC); the third part is its prereqs, which are in the format of a list of sets to represent the AND/OR relationship; forth part is units; fifth one is for quarters they are offering.

    **Note:** I still need more information about the specializations in order to minimize my graph.
4. An Schedule
This schedule takes the quarter offering and course units into account. However, it ignores the time conflict between courses and assigns all courses in the test file to the schedule. It does not perform very well when GE courses are included.

    **sample:**
    ```
    Taking 16 credits per quarter:
    year 1 quarter 1: ['I&CSCI6B', 'I&CSCI31', 'MATH1A', 'I&CSCI90']
    year 1 quarter 2: ['I&CSCI6D', 'I&CSCI51', 'I&CSCI32']
    year 1 quarter 3: ['IN4MATX43', 'I&CSCI53+53L', 'I&CSCI33']
    year 2 quarter 1: ['MATH1B', 'I&CSCI45C']
    year 2 quarter 2: ['MATH2A', 'I&CSCI46']
    year 2 quarter 3: ['MATH2B', 'COMPSCI164']
    year 3 quarter 1: ['MATH3A', 'STATS67', 'COMPSCI161']
    year 3 quarter 2: ['COMPSCI162', 'COMPSCI116', 'COMPSCI178', 'COMPSCI171']
    year 3 quarter 3: ['COMPSCI163', 'COMPSCI165', 'COMPSCI175']
    year 4 quarter 1: ['COMPSCI169']
    year 4 quarter 2: ['COMPSCI167']
    ```

## Schedule

### 2017 Winter Quarter
During winter quarter, I will implement the algorithm and resolve dificulties described. I
will also have a working application done by the end of this quarter.
- **Week 1:** (Done) Find a method to represent the study plan graph.

- **Week 2:** (Done) Apply the basic Coffman-Graham algorithm, which defines a fixed width bound $ W $, and test its performance in this particular course scheduling problem assuming that the number of classes a student takes will not exceed a fixed width bound.

- **week 3:** (In progress) Collect courses information online by using web crawlers or a UCI-Course-API on GitHub.

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