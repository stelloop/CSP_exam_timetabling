import csp
import sys 
import csv
import time


class exam_sched(csp.CSP):
    def __init__(self, days, slots_per_day, file):
        print(slots_per_day)		  
        print(days)
        print(file)
        rows = []
        with open(sys.argv[3], 'r') as f:
            reader = csv.reader(f)
            fields = next(reader)
            for row in reader:
                rows.append(row)
        
        self.semester = []
        self.variables = []
        self.proffesors = []
        self.difficulty = []

        # metadata about the constaints
        self.constaint_checks = 0


        # create slots [day, slotnum] 
        slots = []
        for i in range(1,days+1):
            for j in range(1,slots_per_day+1):
                slots.append((i,j))

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
                self.difficulty.append(False)
                # if row[3] == 'FALSE':     # and the same difficulty too
                #   self.difficulty.append(False)
                # else:
                #   self.difficulty.append(True)

    # create dicts
        self.lesson_to_semester = dict(zip(self.variables,self.semester))
        self.lesson_to_proff = dict(zip(self.variables,self.proffesors))
        self.lesson_to_difficulty = dict(zip(self.variables, self.difficulty))


        # print(self.lesson_to_semester)
        # print(self.lesson_to_proff)
        # print(self.lesson_to_difficulty)



        # create the list of slots for each case
        # if a lesson does not have a lab, it can be assigned on any slot of each day
        lab_not_exists = slots

        # if a lesson has a lab, it can be assigned on either the first or the second slot of each day
        lab_exists = []
        for slot in slots:
            if slot[1] != slots_per_day:
                lab_exists.append(slot)

            is_lab = []
        # the lab of a lesson, it can be assigned on either the second or the third slot of each day
        for slot in slots:
            if slot[1] != 1:
                is_lab.append(slot)


        # print("initializing domains")
        # create the domains of each var.
        # create an empty dict
        self.var_domains = {}
        for lesson in self.variables:

            lab_lesson = 'LAB_' + lesson
            if lab_lesson in self.variables:
                self.var_domains[lesson] = lab_exists
                # print("theory w/ lab lesson: ", lesson)
            else: 
                # check if we are dealing with a lab 
                if 'LAB_' in lesson:
                    self.var_domains[lesson] = is_lab
                    # print("lab lesson: ", lesson)
                else:
                    self.var_domains[lesson] = lab_not_exists

            # create neighbors dict
            self.neighbors_dict = {}
        for lesson in self.variables:
            neighbors = [] # add all the other lessons
            for l in self.variables:
                if l != lesson:
                    neighbors.append(l)
                    self.neighbors_dict[lesson] = neighbors

    

        csp.CSP.__init__(self, self.variables, self.var_domains, self.neighbors_dict, self.constraints)


        self.constaint_checks = 0









    def constraints(self, A, a, B, b):
        self.constaint_checks += 1
        # print("\n")
        # print(A ,"with slot: ", a)
        # print(B ,"with slot: ", b)


        if a == b:  # two lessons can't have the same slots_per_day
            # print("case 1: simple slot conflict")
            prev = self.weights[(A,B)] 
            self.weights[(A,B)] = prev + 1
            return False

        # if A or B is a lab, then for the constraints not to be violated, we must ensure that the previous slot 
        # contains the theory part of the lab 

        if 'LAB_' + A in self.variables: # A is theory lesson that has lab
            if B == 'LAB_' + A: # B is lab
                if (b[0] == a[0]) and (b[1] == (a[1]+1)):
                    return True
                else:
                    # print("tried to assign asxeto after theory-lab lesson")
                    prev = self.weights[(A,B)] 
                    self.weights[(A,B)] = prev + 1
                    return False # keep this slot empty



        if 'LAB_' + B in self.variables: # B is theory lesson that has lab
            if A == 'LAB_' + B: # B is lab
                if (a[0] == b[0]) and (a[1] == (b[1]+1)):
                    return True
                else:
                    # print("tried to assign asxeto after theory-lab lesson")
                    prev = self.weights[(A,B)] 
                    self.weights[(A,B)] = prev + 1
                    return False # keep this slot empty



        # check the other constraints Now
        # check hard lessons constraint (if both lessons are hard)
        if self.lesson_to_difficulty[A] and self.lesson_to_difficulty[B]:
            # print("case 3: both lessons hard")
            if abs(a[0]-b[0]) < 2: # less than two days apart
                prev = self.weights[(A,B)] 
                self.weights[(A,B)] = prev + 1
                return False

        # check semester constraint
        if self.lesson_to_semester[A] == self.lesson_to_semester[B]:
            if abs(a[0]-b[0]) == 0:   # exam on the same day
                # print("case 4: same semester - same day")
                prev = self.weights[(A,B)] 
                self.weights[(A,B)] = prev + 1
                return False  

        # check proffessor constraints
        if self.lesson_to_proff[A] == self.lesson_to_proff[B]:
            if abs(a[0]-b[0]) == 0:   # exam on the same day
                # print("case 5: same day - same proffessor")
                prev = self.weights[(A,B)] 
                self.weights[(A,B)] = prev + 1
                return False  
        # print("constraints OK")      
        return True



  # def domwdeg(self, assignment, csp):
    # # dom/wdeg, var
    # min_var =  (float('inf'), None)

    # for var in self.variables:
    #   # var hasn't gotten a value yet
    #   if var not in self.assignment.keys():  
    #     curr_domain = len(csp.choices(var))
    #     for neighbor in self.neighbors_dict[var]:
    #       print(neighbor)
    #       # both var and its neighbors have not gotten a value yet
    #       if neighbor not in self.assignment.keys():
    #         if (var,neighbor) in self.weights.keys():
    #           wdeg = self.weights[(var,neighbor)]
    #         else: 
    #           wdeg = self.weights[(neighbor,var)]

    #       if curr_domain/wdeg < min_var[0]:
    #         min_var = (curr_domain/wdeg, var)

    # return min_var[1]  






# days slots_per_day input file
if __name__ == '__main__':
  if len(sys.argv) != 4:
    print ("add <days> <slots_per_day> <input file>\n")
    quit()
  else:

    days = int(sys.argv[1])
    slots_per_day = int(sys.argv[2])
    file = sys.argv[3]

    print("creating a new class instance")
    c1 = exam_sched(days, slots_per_day, file)

    
    # # Solution with simple backtracking
    # print("simple BT")
    # start = time.time()
    # bt_result = csp.backtracking_search(c1)
    # end = time.time()
    # print("Time elapsed: %.5f" % (end - start))
    # print("Assignments: ", c1.nassigns)
    # # print("variables: ", c1.variables)
    # # print("constraint checks: ", bt_examsched.conflicted_vars)
    # c1.display(bt_result)

    # for day in range(1,days+1):
    #   print("\t\t\t-------------------------\t")
    #   print("\t\t\t|\tday: ", day,"\t|")
    #   print("\t\t\t-------------------------\t")
    #   for slot in range(1,slots_per_day+1):
    #     t = (day,slot)
    #     for lesson, assignment in bt_result.items():
    #       if t == assignment:
    #         print(t, ": ", lesson)

    # Solution with simple backtracking
    print("simple BT")
    start = time.time()
    bt_result = csp.backtracking_search(c1, select_unassigned_variable=csp.domwdeg,order_domain_values=csp.lcv,inference=csp.forward_checking)
    end = time.time()
    print("Time elapsed: %.5f" % (end - start))
    print("Assignments: ", c1.nassigns)
    print("Constraint checks: ", c1.constaint_checks)
    # print("variables: ", c1.variables)
    # print("constraint checks: ", bt_examsched.conflicted_vars)
    c1.display(bt_result)

    for day in range(1,days+1):
      print("\t\t\t-------------------------\t")
      print("\t\t\t|\tday: ", day,"\t|")
      print("\t\t\t-------------------------\t")
      for slot in range(1,slots_per_day+1):
        t = (day,slot)
        for lesson, assignment in bt_result.items():
          if t == assignment:
            print(t, ": ", lesson)

    quit()



    print("-----------------------------------")


    # quit()

    print("creating a new class instance")
    c2 = exam_sched(days, slots_per_day, file)

    print("BT with MRV, LCV and forward checking")
    start = time.time()
    bt_result = csp.backtracking_search(c2,  select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
    end = time.time()
    print("Time elapsed: %.5f" % (end - start))
    print("Assignments: ", c2.nassigns)
    # print("variables: ", c2.variables)
    # print("constraint checks: ", bt_examsched.conflicted_vars)
    c2.display(bt_result)
    print("-----------------------------------")

    for day in range(1,days+1):
      print("\t\t\t------------------\t")
      print("\t\t\t|\tday: ", day,"|")
      print("\t\t\t------------------\t")
      for slot in range(1,slots_per_day+1):
        t = (day,slot)
        for lesson, assignment in bt_result.items():
          if t == assignment:
            if c2.lesson_to_difficulty[lesson]:
              print(t, ": ", lesson, "HARD")
            else:
              print(t, ": ", lesson)      

    # quit()

    print("creating a new class instance")
    c3 = exam_sched(days, slots_per_day, file)

    # Solution with simple backtracking
    print("BT with MRV and MAC")
    start = time.time()
    bt_result = csp.backtracking_search(c3, select_unassigned_variable=csp.mrv, inference=csp.mac)
    end = time.time()
    print("Time elapsed: %.5f" % (end - start))
    print("Assignments: ", c3.nassigns)
    # print("variables: ", c3.variables)
    # print("constraint checks: ", bt_examsched.conflicted_vars)
    c3.display(bt_result)
    print("-----------------------------------")
    for day in range(1,days+1):
      print("\t\t\t------------------\t\t\t")
      print("\t\t\t|\tday: ", day,"\t|")
      print("\t\t\t------------------\t\t\t")
      for slot in range(1,slots_per_day+1):
        t = (day,slot)
        for lesson, assignment in bt_result.items():
          if t == assignment:
            if c3.lesson_to_difficulty[lesson]:
              print(t, ": ", lesson, "HARD")
            else:
              print(t, ": ", lesson)  




    # quit()


    print("creating a new class instance")
    c4 = exam_sched(days, slots_per_day, file)

    print("BT with MRV, LCV and MINCONFLICTS")
    start = time.time()
    bt_result = csp.min_conflicts(c4)
    end = time.time()
    print("Time elapsed: %.5f" % (end - start))
    print("Assignments: ", c4.nassigns)
    # print("variables: ", c4.variables)
    # print("constraint checks: ", bt_examsched.conflicted_vars)
    c4.display(bt_result)

    print("-----------------------------------")

    for day in range(1,days+1):
      print("\t\t\t------------------\t\t\t")
      print("\t\t\t|\tday: ", day,"\t|")
      print("\t\t\t------------------\t\t\t")
      for slot in range(1,slots_per_day+1):
        t = (day,slot)
        for lesson, assignment in bt_result.items():
          if t == assignment:
            if c4.lesson_to_difficulty[lesson]:
              print(t, ": ", lesson, "HARD")
            else:
              print(t, ": ", lesson)  



    quit()