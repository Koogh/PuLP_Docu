from pulp import *

max_tables = 5
max_table_size = 4
guests = "A B C D E F G I J K L M N O P Q R".split()

def happiness(table):
    """
    Find the happiness of the table
    - by calculating the maximum distance between the letters
    """
    return abs(ord(table[0]) - ord(table[-1]))

# create list of all possible tables
possible_tables = [tuple(c) for c in allcombinations(guests, max_table_size)]

# create a binary variable to state that a table setting is used
x = pulp.LpVariable.dicts("table", possible_tables, lowBound=0, upBound=1, cat=LpInteger)

seating_model = pulp.LpProblem("Wedding Seating Model", LpMaximize)

seating_model += pulp.lpSum([happiness(table) for table in possible_tables]) <= max_tables, "Maximum_number_of_tables"

# A guest must seated at one and only one table
for guest in guests:
    lst = []
    for table in possible_tables:
        if guest in table:
            lst.append(x[table].value())
    seating_model += pulp.lpSum(lst) == 1
    
    
seating_model.solve()

print("The choosen tables are out of a total of %s:" % len(possible_tables))
for table in possible_tables:
    if x[table].value() == 1.0:
        print(table)