from pulp import *

# A list of strings from "1" to "9" is created
Sequence = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# The Vals, Rows and Cols sequences all follow this form
Vals = Sequence
Rows = Sequence
Cols = Sequence

# The boxes list is created, with the row and column index of each sqare in each box
Boxes = []
for i in range(3):
    for j in range(3):
        Boxes += [[(Rows[3*i+k], Cols[3*j+l]) for k in range(3) for l in range(3)]]
   
# Define Problem, in sudoku it can either be LpMinimize or LpMaximize
prob = pulp.LpProblem("Sudoku_Problem", LpMinimize)

# Creating a Set of Variables
choices = pulp.LpVariable.dicts("Choice", (Vals, Rows, Cols), 0,1, LpInteger)

# The arbitrary objective function is added
# prob += 0, "Arbitrary Objective Function"
prob += pulp.lpSum(0)

# A constraint ensuring that only one value can be in each square is created
for r in Rows:
    for c in Cols:
        prob += pulp.lpSum([choices[v][r][c] for v in Vals]) == 1, ""
        
# The row, column and box constraints are added for each value
for v in Vals:
    for r in Rows:
        prob += pulp.lpSum([choices[v][r][c] for c in Cols]) == 1, ""

    for c in Cols:
        prob += pulp.lpSum([choices[v][r][c] for r in Rows]) == 1, ""
        
    for b in Boxes:
        prob += pulp.lpSum([choices[v][r][c] for (r,c) in b]) == 1, ""
        

######## Given Problem ########

input_data = [
    ("5", "1", "1"),
    ("6", "2", "1"),
    ("8", "4", "1"),
    ("4", "5", "1"),
    ("7", "6", "1"),
    ("3", "1", "2"),
    ("9", "3", "2"),
    ("6", "7", "2"),
    ("8", "3", "3"),
    ("1", "2", "4"),
    ("8", "5", "4"),
    ("4", "8", "4"),
    ("7", "1", "5"),
    ("9", "2", "5"),
    ("6", "4", "5"),
    ("2", "6", "5"),
    ("1", "8", "5"),
    ("8", "9", "5"),
    ("5", "2", "6"),
    ("3", "5", "6"),
    ("9", "8", "6"),
    ("2", "7", "7"),
    ("6", "3", "8"),
    ("8", "7", "8"),
    ("7", "9", "8"),
    ("3", "4", "9"),
    ("1", "5", "9"),
    ("6", "6", "9"),
    ("5", "8", "9"),
]

for (v,r,c) in input_data:
    prob += choices[v][r][c]==1, ""
    # print( v,r,c)

# The problem data is written to an .lp file
prob.writeLP("Sudoku.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# The solution is written to the sudokuout.txt file
sudokuout = open('sudokuout.txt','w')

# The solution is written to the sudokuout.txt file 
for r in Rows:
    if r == "1" or r == "4" or r == "7":
                    sudokuout.write("+-------+-------+-------+\n")
    for c in Cols:
        for v in Vals:
            if value(choices[v][r][c])==1:
                               
                if c == "1" or c == "4" or c =="7":
                    sudokuout.write("| ")
                    
                sudokuout.write(v + " ")
                
                if c == "9":
                    sudokuout.write("|\n")
sudokuout.write("+-------+-------+-------+")                    
sudokuout.close()
                    
        