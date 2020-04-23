import tkinter
from collections import deque
from itertools import groupby
from typing import List, Union, Optional

# Same type aliases
Lit = int
Var = int
Clause = List[int]
CNF = List[Clause]
Assignment = List[Optional[bool]]

# FOR DEBUGGING:
# Replace this with a CNF that breaks your solver (don't forget to change n)
#n = 4
#cnf = [[-1, -2], [-1, 2, 3], [-3, -4], [1, 2, 3], [-3], [1, -2], [2, -3], [1, -2, 3]]
#cnf = [[-1, -2], [-1, 2, 3], [-3, -4]]


def preprocess(cnf: CNF) -> CNF:
    """Remove duplicate literals and clauses from a CNF formula."""
    cnf = [list(set(clause)) for clause in cnf]
    cnf.sort()
    return list(clause for clause, _ in groupby(cnf))


def lit(variable: Var, value: bool) -> Lit:
    """ Accepts a variable x and a value. Returns the positive literal (`x`) if the value
    is True, otherwise returns the negative literal (`-x`). """
    return variable if value else -variable


def bsign(literal: Lit, value: bool) -> Optional[bool]:
    """
    Accepts a literal and a boolean value. If the literal is positive, the value is
    returned; if the literal is negative, the negation of the value is returned.
    If the value is None, however, the function always returns None.

    You can interpret this as "the value of the given literal if its corresponding
    variable has the given value".
    """
    return None if value is None else value if literal > 0 else not value


class IterativePennSAT():
    """A DPLL-based SAT solver with 2 watched literals and a static activity decision heuristic."""

    def __init__(self, n: int, cnf: CNF, activity_heuristic: bool = True):
        # The number of variables
        self.n = n
        # The CNF as a list of clauses
        self.cnf: CNF = preprocess(cnf)
        # A stack of partial truth assignments: lists mapping each variable to True/False/None
        self.assignment_stack: List[Assignment] = [[None] * (n + 1)]
        if activity_heuristic:
            # We'll implement this function later
            self.var_ordering = self.compute_activity_ordering()
        else:
            self.var_ordering = list(range(1, n + 1))
        # A stack of decision variables
        self.decision_stack: List[Var] = []
        # For each literal, a queue of all clauses watching that literal
        self.clauses_watching: List[deque] = [deque() for i in range(2 * n + 1)]
        # A queue of literals which have been assumed `False`
        self.propagation_queue: deque = deque()
        # A switch for processive DPLL
        self.decision = 0
        self.next = 1
        self.in_loop = 1
        self.sat = []

        self.check_all_set = False
        self.check_unit_prop = False
        self.check_level_0 = False
        self.skip_this = False


        # initialize clauses watching
        for claws in self.cnf:
            self.clauses_watching[claws[0]].append(claws)
            if (len(claws) == 1):
                continue
            else:
                self.clauses_watching[claws[1]].append(claws)

    def value(self, literal: Lit) -> Optional[bool]:
        """Returns the value of the literal (`True`/`False`/`None`) under the current assignment."""
        return bsign(literal, self.assignment_stack[-1][abs(literal)])

    def assume(self, literal: Lit) -> bool:
        """Assign the literal to `True` in the current assignment and add its negation to the
        propagation queue. Returns False if the literal was already assigned to `False`;
        otherwise returns True."""
        print("assuming " + str(literal))
        if self.value(literal) is False:
            print(str(literal) + " was false")
            return False
        elif self.value(literal) is True:
            print(str(literal) + " was true")
            return True
        else:
            self.assignment_stack[-1][abs(literal)] = bsign(literal, True)
            self.propagation_queue.append(literal * -1)
            print(str(literal) + " was unassigned, " + str(-1 * literal) + " added to propogation queue")
            return True

    def compute_activity_ordering(self) -> List[Var]:
        """Returns a list of variables [1..n] sorted by descending activity score
        based on the stored CNF."""
        cnf = self.cnf
        n = self.n
        # Fill in your implementation here
        totals = [0 for i in range(n + 1)]
        for clause in cnf:
            factor = 1 / (2 ** len(clause))
            for lit in clause:
                totals[abs(lit)] += factor
        original_totals = totals.copy()
        totals = totals[1:]
        totals = sorted(totals, reverse=True)
        vars = []
        for total in totals:
            temp_index = original_totals.index(total)
            vars.append(temp_index)
            original_totals[temp_index] = -1
        return vars

    def pick_variable(self) -> Optional[Var]:
        """Returns the first unassigned variable in the stored variable ordering,
        or `None` if all variables have been assigned."""
        print("picking variable")
        # Fill in your implementation here
        for i in range(len(self.var_ordering)):
            index = self.var_ordering[i]
            if self.assignment_stack[-1][index] is None:
                return index
        return None

    def propagate_from(self, false_literal: Lit) -> bool:
        print("progagating from literal " + str(false_literal))
        """
        Accepts as input a literal which has been assigned to `False`, and updates the
        watched literals of every clause previously watching that literal in order to
        maintain the 2 Watched Literals invariant, performing unit propagation as needed.

        Returns `False` if a conflict occurs; otherwise `True`.
        """
        # Repeat once for each clause initially watching the false literal
        print("checking each clause watching " + str(false_literal))
        for _ in range(len(self.clauses_watching[false_literal])):
            clause = self.clauses_watching[false_literal].popleft()
            print("current clause: " + str(clause))

            # If the clause is now empty
            if len(clause) == 1:
                print("clause now empty, conflict")
                return False
            # Make the false literal the second watched literal (for convenience)
            if clause[1] != false_literal:
                clause[0], clause[1] = clause[1], clause[0]
            if self.value(clause[0]) is True:
                self.clauses_watching[false_literal].append(clause)
                continue
            # Fill in the rest of your implementation here
            for i in range(2, len(clause)):
                literal = clause[i]
                if self.value(literal) is not False:
                    clause[1], clause[i] = clause[i], clause[1]
                    self.clauses_watching[clause[1]].append(clause)
                    break
            else:
                self.clauses_watching[false_literal].append(clause)
                if self.assume(clause[0]) is False:
                    return False
        return True

    def unit_propagate(self) -> bool:
        print("called unit_propogate, propagating from every literal on propogation queue")
        print(self.propagation_queue)
        """
        Calls `propagate_from()` on every literal in the propagation queue
        until the queue is empty. If we ever encounter a conflict, this
        returns `False`; otherwise `True`.
        """
        # Fill in your implementation here
        while self.propagation_queue:
            literal = self.propagation_queue.popleft()
            if (self.propagate_from(literal) is False):
                return False
        return True

    def backtrack_and_assume_negation(self) -> None:
        """Undo the last decision and restore the previous partial assignment.
        Then assume the negation of the last decision variable."""
        # Fill in your implementation here
        print("backtrack and assume negation")
        self.assignment_stack.pop()
        self.propagation_queue = deque()
        if not self.decision_stack: return
        last_decision = self.decision_stack.pop()
        self.assume(-1 * last_decision)
        return

    def solve(self) -> Union[str, List[Lit]]:
        """Return a satisfying assignment to the stored CNF, or return `'UNSAT'` if none exists."""
        # Fill in your implementation here
        if self.next == 1:
            print("checking for unit clauses")
            for clause in self.cnf:
                if len(clause) == 1:
                    print("found unit clause: " + str(clause[0]))
                    if self.assume(clause[0]) is False:
                        return "UNSAT"
            self.switch = -1
            self.next = 2
            return 'image1'

        # for assignment in self.assignment_stack[-1]:

        if self.next == 2:
            if not self.unit_propagate():
                return 'UNSAT'
            self.switch = -1
            self.next = 3
            self.check_all_set = True
            # return 'image2'

        # just checked if all set, not going to
        if self.check_all_set:
            self.check_all_set = False
            local_sat = self.assignment_stack[-1]
            print(local_sat, 'hey peter')
            for index, var in enumerate(local_sat[1:]):
                if var is None and index in self.var_ordering and index != 0:
                    print(var, "AHHHHHHH\n\n\n\n")
                    break
            else:
                self.sat = [lit(x, self.value(x)) for x in range(1, self.n + 1)]
                return 'SAT'
            return 'image3'

        if self.next == 3:
            if (self.switch == 1) :
                self.switch = -1
                print('fricken stall')
                return 'image4'

            while True:
                if self.in_loop == 1:
                    self.decision = self.pick_variable()
                    if self.decision is None:
                        print("all variables are assigned")
                        self.check_all_set = True
                        #self.switch = 1
                        return 'image2'
                        break
                    print("picked variable " + str(self.decision) + ", appending to decision stack")
                    self.decision_stack.append(self.decision)
                    new_assignment = self.assignment_stack[-1].copy()
                    print(new_assignment)
                    self.assignment_stack.append(new_assignment)
                    self.in_loop = 2
                    self.switch = -1

                    # local_sat = [lit(x, self.value(x)) for x in range(1, self.n + 1)]
                    # print(local_sat, 'hey peter2')
                    # for var in local_sat[1:]:
                    #     if var is None or var < 0:
                    #         break
                    # else:
                    #     self.check_all_set = True

                    #return

                if self.in_loop == 2:
                    self.assume(self.decision)
                    self.in_loop = 3
                    self.switch = -1
                    print("here")
                    if not (self.skip_this):
                        self.skip_this = True
                        return 'image4'

                if self.in_loop == 3:
                    print("here again")
                    if not self.check_unit_prop:
                        # if not self.check_level_0:
                        #     self.check_level_0 = True
                        if not self.unit_propagate():
                            self.check_unit_prop = True
                            return 'image5'
                        else:
                            self.in_loop = 1
                            self.check_all_set = True
                            self.skip_this = False
                            return 'image2'
                                # print("in loop 3")
                                # self.backtrack_and_assume_negation()
                                # if len(self.assignment_stack) == 0:
                                #     return 'UNSAT'
                                # else:
                                #     print('what???')
                                #     return 'image5'
                    else:
                        if not self.check_level_0:
                            self.check_level_0 = True
                            if len(self.assignment_stack) == 1:
                                return 'UNSAT'
                            else:
                                print('what???')
                                return 'image6'
                        else:
                            self.check_level_0 = False
                            print('hi Joe Swanson')
                            self.in_loop = 2
                            #self.switch = -1
                            self.check_unit_prop = False

                            self.backtrack_and_assume_negation()


                            return 'image4'
                    # else:
                    #     self.check_unit_prop = False
                    #
                    #     print('please?')
                    #     self.in_loop = 1
                    #
                    #     self.switch = 1
                    #     self.in_loop = 1
                    #     self.check_all_set = True
                    #     print('Family guy is epic')
                    #     return 'image3'
            self.sat = [lit(x, self.value(x)) for x in range(1, self.n + 1)]
            return "SAT"



    def start(self):
        for clause in self.cnf:
            if len(clause) == 1:
                if self.assume(clause[0]) is False:
                    return "UNSAT"
        return "not yet"


# solver = IterativePennSAT(n, cnf, True)
# x = solver.solve()
# while not (x == "UNSAT" or x == "SAT"):
#     x = solver.solve()
# print(x + ", satisfying assignment: " + str(solver.sat))
