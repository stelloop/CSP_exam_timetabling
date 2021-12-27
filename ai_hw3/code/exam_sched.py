import csp
import sys 
import csv
import time


class exam_sched(csp.CSP):
    def __init__(self, days, slots_per_day, file):
        # read the contents of the .csv file
        rows = []
        with open(file, 'r') as f:
            reader = csv.reader(f)
            fields = next(reader)
            for row in reader:
                rows.append(row)

        # info from the csv file
        self.semester = []
        self.variables = []
        self.proffesors = []
        self.difficulty = []





        for row in rows:
            self.semester.append(int(row[0]))
            self.variables.append(row[1])
            self.proffesors.append(row[2])
            if row[3] == 'FALSE':
                self.difficulty.append(False)
            else:
                self.difficulty.append(True)
            if row[4] == 'TRUE':
                # lesson has lab, create a new lesson, adding prefix "LAB_"
                new_lesson = 'LAB_' + row[1]
                self.variables.append(new_lesson)
                self.proffesors.append(row[2]) # lab has the same proffessor
                self.semester.append(int(row[0])) # the same semester
                self.difficulty.append(False)  # a lab has no degree of difficulty

        # create dicts
        self.lesson_to_semester = dict(zip(self.variables,self.semester))
        self.lesson_to_proff = dict(zip(self.variables,self.proffesors))
        self.lesson_to_difficulty = dict(zip(self.variables, self.difficulty))

        # create slots [day, slotnum] 
        slots = []
        for i in range(1,days+1):
            for j in range(1,slots_per_day+1):
                slots.append((i,j))

        # if a lesson does not have a lab, it can be assigned on any slot of each day
        lab_not_exists = slots

        # if a lesson has a lab, it can be assigned on all slots except of the last one of each day
        lab_exists = []
        for slot in slots:
            if slot[1] != slots_per_day:
                lab_exists.append(slot)

        is_lab = []
        # the lab of a lesson, it can be assigned on all slots except of the first one of each day
        for slot in slots:
            if slot[1] != 1:
                is_lab.append(slot)


        # assign the appropriate domains for each var.
        # create an empty dict
        self.var_domains = {}
        for lesson in self.variables:

            lab_lesson = 'LAB_' + lesson
            if lab_lesson in self.variables:  # theory lesson has lab
                self.var_domains[lesson] = lab_exists
            else: 
                # check if we are dealing with a lab 
                if 'LAB_' in lesson:
                    self.var_domains[lesson] = is_lab
                else:
                    self.var_domains[lesson] = lab_not_exists

        # create neighbors dict
        self.neighbors_dict = {}
        for lesson in self.variables:
            neighbors = [] # add all the other lessons, except of itself
            for l in self.variables:
                if l != lesson:
                    neighbors.append(l)
                    self.neighbors_dict[lesson] = neighbors

    
        # init total constraint checks
        self.constraint_checks = 0
        csp.CSP.__init__(self, self.variables, self.var_domains, self.neighbors_dict, self.constraints)

    def constraints(self, A, a, B, b):
        self.constraint_checks += 1

        # two lessons can't have the same slots_per_day
        if a == b:  
            prev = self.weights[(A,B)] # needed for dom/wdeg 
            self.weights[(A,B)] = prev + 1
            return False

        # if A or B is a lab, then for the constraints not to be violated, we must ensure that the previous slot 
        # contains the theory part of the lab 
        if 'LAB_' + A in self.variables: # A is theory lesson that has lab
            if B == 'LAB_' + A: # B is lab
                if (b[0] == a[0]) and (b[1] == (a[1]+1)): # lab is right after theory
                    return True
                else:
                    prev = self.weights[(A,B)] 
                    self.weights[(A,B)] = prev + 1
                    return False # keep this slot empty



        if 'LAB_' + B in self.variables: # B is theory lesson that has lab
            if A == 'LAB_' + B: # B is lab
                if (a[0] == b[0]) and (a[1] == (b[1]+1)):
                    return True
                else:
                    prev = self.weights[(A,B)] 
                    self.weights[(A,B)] = prev + 1
                    return False # keep this slot empty

        # check hard lessons constraint (if both lessons are hard)
        if self.lesson_to_difficulty[A] and self.lesson_to_difficulty[B]:
            if abs(a[0]-b[0]) < 2: # less than two days apart
                prev = self.weights[(A,B)] 
                self.weights[(A,B)] = prev + 1
                return False

        # check semester constraint
        if self.lesson_to_semester[A] == self.lesson_to_semester[B]:
            if abs(a[0]-b[0]) == 0:   # exam on the same day
                prev = self.weights[(A,B)] 
                self.weights[(A,B)] = prev + 1
                return False  

        # check proffessor constraints
        if self.lesson_to_proff[A] == self.lesson_to_proff[B]:
            if abs(a[0]-b[0]) == 0:   # exam on the same day
                prev = self.weights[(A,B)] 
                self.weights[(A,B)] = prev + 1
                return False  
        return True # none of the constraints were violated




if __name__ == '__main__':
  if len(sys.argv) != 6:
    print ("usage: python3 exam_sched.py <days> <slots_per_day> <input file> <fc or mac or min-conflicts> <mrv or domwdeg or None (for min-conflicts)>\n")
    quit()
  else:
    # read the args
    days = int(sys.argv[1])
    slots_per_day = int(sys.argv[2])
    file = sys.argv[3]
    algo = sys.argv[4]
    heur = sys.argv[5]


    # create an instance of our class
    c1 = exam_sched(days, slots_per_day, file)
    res = None
    if algo == 'fc':
        if heur == 'domwdeg':
            print("backtracking with dom/wdeg and MAC")
            start = time.time()
            res = csp.backtracking_search(c1, select_unassigned_variable=csp.domwdeg,order_domain_values=csp.lcv,inference=csp.forward_checking)
            end = time.time()
            print("Time elapsed: %.5f" % (end - start))
            print("Assignments: ", c1.nassigns)
            print("Constraint checks: ", c1.constraint_checks)
        elif heur == 'mrv':
            print("backtracking with MRV and MAC")
            start = time.time()
            res = csp.backtracking_search(c1, select_unassigned_variable=csp.mrv,order_domain_values=csp.lcv,inference=csp.forward_checking)
            end = time.time()
            print("Time elapsed: %.5f" % (end - start))
            print("Assignments: ", c1.nassigns)
            print("Constraint checks: ", c1.constraint_checks)
        else:
            print(heur, " is not an acceptable argument. Please give correct arguments!")
            print ("usage: python3 exam_sched.py <days> <slots_per_day> <input file> <fc or mac or min-conflicts> <mrv or domwdeg>\n")
            quit()
    elif algo == 'mac':
        if heur == 'domwdeg':
            print("backtracking with dom/wdeg and MAC")
            start = time.time()
            res = csp.backtracking_search(c1, select_unassigned_variable=csp.domwdeg,order_domain_values=csp.lcv,inference=csp.mac)
            end = time.time()
            print("Time elapsed: %.5f" % (end - start))
            print("Assignments: ", c1.nassigns)
            print("Constraint checks: ", c1.constraint_checks)
        elif heur == 'mrv':
            print("backtracking with MRV and FC")
            start = time.time()
            res = csp.backtracking_search(c1, select_unassigned_variable=csp.mrv,order_domain_values=csp.lcv,inference=csp.mac)
            end = time.time()
            print("Time elapsed: %.5f" % (end - start))
            print("Assignments: ", c1.nassigns)
            print("Constraint checks: ", c1.constraint_checks)
        else:
            print(heur, " is not an acceptable argument. Please give correct arguments!")
            print ("usage: python3 exam_sched.py <days> <slots_per_day> <input file> <fc or mac or min-conflicts> <mrv or domwdeg>\n")
            quit()
    elif algo == 'min-conflicts':
            print("MinConflicts")
            start = time.time()
            res = csp.min_conflicts(c1)
            end = time.time()
            print("Time elapsed: %.5f" % (end - start))
            print("Assignments: ", c1.nassigns)
            print("Constraint checks: ", c1.constraint_checks)
    else:
        print(algo, " is not an acceptable argument. Please give correct arguments!")
        print ("usage: python3 exam_sched.py <days> <slots_per_day> <input file> <fc or mac or min-conflicts> <mrv or domwdeg>\n")
        quit()
    for day in range(1,days+1):
      print("\t\t\t-------------------------\t")
      print("\t\t\t|\tday: ", day,"\t|")
      print("\t\t\t-------------------------\t")
      for slot in range(1,slots_per_day+1):
        t = (day,slot)
        for lesson, assignment in res.items():
          if t == assignment:
            if c1.lesson_to_difficulty[lesson]:
              print(t, ": ", lesson, " [difficult]", " semester: ", c1.lesson_to_semester[lesson], " proffessor: ", c1.lesson_to_proff[lesson])
            else:
              print(t, ": ", lesson, " [easy]", " semester: ", c1.lesson_to_semester[lesson], " proffessor: ", c1.lesson_to_proff[lesson])    
