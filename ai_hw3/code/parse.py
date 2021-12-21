import csv

rows = []
with open('../input.csv', 'r') as f:
  reader = csv.reader(f)
  fields = next(reader)
  print("fields are:")
  print(fields)
  print("\n")
  for row in reader:
    rows.append(row)

# print(rows)

semester = []
lessons = []
proffesors = []
difficulty = []

total_days = 21
slots_per_day = 3
# create slots [day, slotnum] 
slots = []
for i in range(1,total_days+1):
  for j in range(1,slots_per_day+1):
    slots.append([i,j])



# print(slots)







for row in rows:
  semester.append(int(row[0]))
  lessons.append(row[1])
  proffesors.append(row[2])
  if row[3] == 'FALSE':
    difficulty.append(False)
  else:
    difficulty.append(True)
  if row[4] == 'TRUE':
    # lesson has lab, create a new lesson, adding prefix "LAB_"
    new_lesson = 'LAB_' + row[1]
    lessons.append(new_lesson)
    proffesors.append(row[2]) # lab has the same proffessor
    semester.append(int(row[0])) # the same semester
    if row[3] == 'FALSE':     # and the same difficulty too
      difficulty.append(False)
    else:
      difficulty.append(True)



# create dicts
lesson_to_semester = dict(zip(lessons,semester))
lesson_to_proff = dict(zip(lessons,proffesors))
lesson_to_difficulty = dict(zip(lessons, difficulty))


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
var_domains = {}
for lesson in lessons:
  print(lesson)

  lab_lesson = 'LAB_' + lesson
  if lab_lesson in lessons:
    print("has lab")
    var_domains[lesson] = lab_exists
  else: 
    # check if we are dealing with a lab 
      if 'LAB_' in lesson:
        var_domains[lesson] = is_lab
      else:
        var_domains[lesson] = lab_not_exists




print(var_domains)

# create neighbors dict
neighbors_dict = {}
for lesson in lessons:
  neighbors = [] # add all the other lessons
  for l in lessons:
    if l != lesson:
      neighbors.append(l)
  neighbors_dict[lesson] = neighbors















# print("semesters:")
# print(semester)



# print("profs:")
# print(proffesors)

# print("diff")
# print(difficulty)

# print("lab")
# print(lab)
