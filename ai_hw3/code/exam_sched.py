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
    self.lessons = []
    self.proffesors = []
    self.difficulty = []

    # create slots [day, slotnum] 
    slots = []
    for i in range(1,days+1):
      for j in range(1,slots_per_day+1):
          slots.append((i,j))

    for row in rows:
      self.semester.append(int(row[0]))
      self.lessons.append(row[1])
      self.proffesors.append(row[2])
      if row[3] == 'FALSE':
        self.difficulty.append(False)
      else:
        self.difficulty.append(True)
      if row[4] == 'TRUE':
        # lesson has lab, create a new lesson, adding prefix "LAB_"
        new_lesson = 'LAB_' + row[1]
        self.lessons.append(new_lesson)
        self.proffesors.append(row[2]) # lab has the same proffessor
        self.semester.append(int(row[0])) # the same semester
        if row[3] == 'FALSE':     # and the same difficulty too
          self.difficulty.append(False)
        else:
          self.difficulty.append(True)

  # create dicts
    self.lesson_to_semester = dict(zip(self.lessons,self.semester))
    self.lesson_to_proff = dict(zip(self.lessons,self.proffesors))
    self.lesson_to_difficulty = dict(zip(self.lessons, self.difficulty))


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


        # create the domains of each var.
    # create an empty dict
    self.var_domains = {}
    for lesson in self.lessons:

      lab_lesson = 'LAB_' + lesson
      if lab_lesson in self.lessons:
        self.var_domains[lesson] = lab_exists
      else: 
        # check if we are dealing with a lab 
          if 'LAB_' in lesson:
            self.var_domains[lesson] = is_lab
          else:
            self.var_domains[lesson] = lab_not_exists

    # create neighbors dict
    self.neighbors_dict = {}
    for lesson in self.lessons:
      neighbors = [] # add all the other lessons
      for l in self.lessons:
        if l != lesson:
          neighbors.append(l)
      self.neighbors_dict[lesson] = neighbors

    csp.CSP.__init__(self, self.lessons, self.var_domains, self.neighbors_dict, self.constraints)



  def constraints(self, A, a, B, b):

    if a == b:  # two lessons can't have the same slots_per_day
      # print("case 1: simple slot conflict")
      return False

    # if A or B is a lab, then for the constraints not to be violated, we must ensure that the previous slot 
    # contains the theory part of the lab 

    if 'LAB_' + A in self.lessons: # A is theory lesson that has lab
      # f"{A} has lab"
      if (b[0] == a[0]) and (b[1] == (a[1]+1)):  # b is the next slot of a
        if B == 'LAB_' + A: # B is lab
          return True 
        else:
          return False # keep this slot empty

    if 'LAB_' + B in self.lessons: # B is theory lesson that has lab
      # f"{B} has lab"
      if (a[0] == b[0]) and (a[1] == (b[1]+1)):  # a is the next slot of a
        if A == 'LAB_' + B: # A is lab
          return True 
        else:
          return False # keep this slot empty
    

    # check the other constraints Now
    # check hard lessons constraint (if both lessons are hard)
    if self.lesson_to_difficulty[A] and self.lesson_to_difficulty[B]:
      # print("case 3: both lessons hard")
      if abs(a[0]-b[0]) < 2: # less than two days apart
        return False

    # check semester constraint
    if self.lesson_to_semester[A] == self.lesson_to_semester[B]:
      if abs(a[0]-b[0]) == 0:   # exam on the same day
        # print("case 4: same semester - same day")
        return False  

    # check proffessor constraints
    if self.lesson_to_proff[A] == self.lesson_to_proff[B]:
      if abs(a[0]-b[0]) == 0:   # exam on the same day
        # print("case 5: same day - same proffessor")
        return False  
    # print("constraints OK")      
    return True

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

    
    # Solution with simple backtracking
    print("simple BT")
    start = time.time()
    bt_result = csp.backtracking_search(c1)
    end = time.time()
    print("Time elapsed: %.5f" % (end - start))
    print("Assignments: ", c1.nassigns)
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





    print("-----------------------------------")


    quit()

    # Solution with simple backtracking
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
      print("\t\t\t------------------\t\t\t")
      print("\t\t\t|\tday: ", day,"\t|")
      print("\t\t\t------------------\t\t\t")
      for slot in range(1,slots_per_day+1):
        t = (day,slot)
        for lesson, assignment in bt_result.items():
          if t == assignment:
            print(t, ": ", lesson)



    quit()

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


    quit()