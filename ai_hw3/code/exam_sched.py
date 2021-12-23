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
          slots.append([i,j])

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
      print(lesson)

      lab_lesson = 'LAB_' + lesson
      if lab_lesson in self.lessons:
        print("has lab")
        self.var_domains[lesson] = lab_exists
      else: 
        # check if we are dealing with a lab 
          if 'LAB_' in lesson:
            self.var_domains[lesson] = is_lab
          else:
            self.var_domains[lesson] = lab_not_exists

    # print(self.var_domains)

    # print(self.lessons)

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


    # print("in constr")
    # print(A)
    # print(a)

    # print(B)
    # print(b)

    if a == b:  # two lessons can't have the same slots_per_day
      # print("case 1: simple slot conflict")
      return False

    # if A or B is a lab, then for the constraints not to be violated, we must ensure that the previous slot 
    # contains the theory part of the lab 

    # βρες πιο απο τα Α,Β ειναι το lab
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
    
    # # we are dealing with a lab, and with a lessin with no lab
    # if 'LAB'



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



    # probably nonsense


    # if 'LAB' + B in self.lessons:
    #   f"{B} has lab"

    


    # if 'LAB_' in B:

    #   print("case 2: at least one of the lessons is a lab")

  

    #   # check lab constraints first (A has lab and b is the lab or vice versa)
    #   if ('LAB_' in B and ('LAB_' + A) != B):
    #     return False
    #   else: 
    #     print("constraints OK")
    #     return True
    # else:
    #   # check hard lessons constraint (if both lessons are hard)
    #   if self.lesson_to_difficulty[A] and self.lesson_to_difficulty[B]:
    #     print("case 3: both lessons hard")
    #     if abs(a[0]-b[0]) < 2: # less than two days apart
    #       return False

    #   # check semester constraint
    #   if self.lesson_to_semester[A] == self.lesson_to_semester[B]:
    #     if abs(a[0]-b[0]) == 0:   # exam on the same day
    #       print("case 4: same semester - same day")
    #       return False  

    #   # check proffessor constraints
    #   if self.lesson_to_proff[A] == self.lesson_to_proff[B]:
    #     if abs(a[0]-b[0]) == 0:   # exam on the same day
    #       print("case 5: same day - same proffessor")
    #       return False  
    # print("constraints OK")      
    # return True










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
    bt_examsched = exam_sched(days, slots_per_day, file)

    
    # Solution with backtracking
    print("BT")
    start = time.time()
    bt_result = csp.backtracking_search(bt_examsched, inference=csp.forward_checking)
    end = time.time()
    print("Time elapsed: %.5f" % (end - start))
    print("Assignments: ", bt_examsched.nassigns)
    print("variables: ", bt_examsched.variables)
    # print("constraint checks: ", bt_examsched.conflicted_vars)
    bt_examsched.display(bt_result)
    print("-----------------------------------")


    # rows = []
    # with open(sys.argv[3], 'r') as f:
    #   reader = csv.reader(f)
    #   fields = next(reader)
    #   for row in reader:
    #     rows.append(row)

    # # print(rows)

    # semester = []
    # lessons = []
    # proffesors = []
    # difficulty = []

    # # create slots [day, slotnum] 
    # slots = []
    # for i in range(1,days+1):
    #   for j in range(1,slots_per_day+1):
    #     slots.append([i,j])

  # for row in rows:
  #   semester.append(int(row[0]))
  #   lessons.append(row[1])
  #   proffesors.append(row[2])
  #   if row[3] == 'FALSE':
  #     difficulty.append(False)
  #   else:
  #     difficulty.append(True)
  #   if row[4] == 'TRUE':
  #     # lesson has lab, create a new lesson, adding prefix "LAB_"
  #     new_lesson = 'LAB_' + row[1]
  #     lessons.append(new_lesson)
  #     proffesors.append(row[2]) # lab has the same proffessor
  #     semester.append(int(row[0])) # the same semester
  #     if row[3] == 'FALSE':     # and the same difficulty too
  #       difficulty.append(False)
  #     else:
  #       difficulty.append(True)


  # # create dicts
  # lesson_to_semester = dict(zip(lessons,semester))
  # lesson_to_proff = dict(zip(lessons,proffesors))
  # lesson_to_difficulty = dict(zip(lessons, difficulty))


  # # create the list of slots for each case
  # # if a lesson does not have a lab, it can be assigned on any slot of each day
  # lab_not_exists = slots

  # # if a lesson has a lab, it can be assigned on either the first or the second slot of each day
  # lab_exists = []
  # for slot in slots:
  #   if slot[1] != slots_per_day:
  #     lab_exists.append(slot)

  # is_lab = []
  # # the lab of a lesson, it can be assigned on either the second or the third slot of each day
  # for slot in slots:
  #   if slot[1] != 1:
  #     is_lab.append(slot)





  # # create the domains of each var.
  # # create an empty dict
  # var_domains = {}
  # for lesson in lessons:
  #   print(lesson)

  #   lab_lesson = 'LAB_' + lesson
  #   if lab_lesson in lessons:
  #     print("has lab")
  #     var_domains[lesson] = lab_exists
  #   else: 
  #     # check if we are dealing with a lab 
  #       if 'LAB_' in lesson:
  #         var_domains[lesson] = is_lab
  #       else:
  #         var_domains[lesson] = lab_not_exists




  # # print(var_domains)

  # # create neighbors dict
  # neighbors_dict = {}
  # for lesson in lessons:
  #   neighbors = [] # add all the other lessons
  #   for l in lessons:
  #     if l != lesson:
  #       neighbors.append(l)
  #   neighbors_dict[lesson] = neighbors






