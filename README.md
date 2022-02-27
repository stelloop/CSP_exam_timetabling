This repo contains an attempt to solve a fairly simple version of exam timetabling, a basic CSP problem.

The constraints to be satisfied are:
- exam period cannot be longer than `num_days` long (consecutive days)
- each lesson's exam duration is 3 hours
- there are `num_slots` time slots for each day
- we have only one available exam room, so we can't have two lesson examinations at the same time
- if a lesson has a theory part and a lab part, the lab part should be examined immidiately after the theory part
- difficult lesson examinations should be at least one day apart
- lessons being taught from the same professor, can't be examined in the same day
- if two lessons are being taught in the same semester, their examination can't be on the same day


Code from https://github.com/aimacode/aima-python/blob/master/csp.py is used. 
Also an `dom/wdeg` implementation (variable ordering heuristic) has been added, based on this paper:  http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf

In order to run the program, the input must be in CSV format, where:
- 1st column: semester
- 2nd column: lesson name
- 3rd column: professor
- 4th column: difficulty(TRUE/FALSE)
- 5th column: lab part(TRUE/FALSE)


Simply type (with the appropriate arguments):
`python3 exam_sched.py <days> <slots> <inputfile path>
<fc/mac/min-conflicts> <mrv/domwdeg>`
