import tkinter
from collections import deque
from itertools import groupby
from typing import List, Union, Optional


Lit = int
Var = int
Clause = List[int]
CNF = List[Clause]
Assignment = List[Optional[bool]]


class Node:
    def __init__(self, text):
        self.left = None
        self.right = None
        self.decision_var = 0
        self.text = text


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

        self.n = n

        self.cnf: CNF = preprocess(cnf)

        self.assignment_stack: List[Assignment] = [[None] * (n + 1)]
        if activity_heuristic:

            self.var_ordering = self.compute_activity_ordering()
        else:
            self.var_ordering = list(range(1, n + 1))

        self.decision_stack: List[Var] = []

        self.clauses_watching: List[deque] = [
            deque() for i in range(2 * n + 1)]

        self.propagation_queue: deque = deque()

        self.decision = 0
        self.next = 1
        self.in_loop = 1
        self.sat = []

        self.check_all_set = False
        self.check_unit_prop = False
        self.check_level_0 = False
        self.skip_this = False

        root = Node('root')
        self.tree_info = root
        self.curr_child = root
        self.last_decision = root
        self.curr_direction = None

        self.first = True
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

        if self.value(literal) is False:
            if (self.curr_child.decision_var != literal and self.curr_child.text != 'root'):
                new_node = Node('CONFLICT')
                new_node.decision_var = literal
                if (self.curr_direction == 'Right'):
                    self.curr_child.right = new_node
                else:
                    self.curr_child.left = new_node
                self.curr_child = new_node
            self.curr_direction = 'Right'

            return False
        elif self.value(literal) is True:

            if (self.curr_child.decision_var != literal and self.curr_child.text != 'root'):
                new_node = None
                if self.first:
                    new_node = Node('initial UP')
                else:
                    new_node = Node('UP')
                new_node.decision_var = literal
                if (self.curr_direction == 'Right'):
                    self.curr_child.right = new_node
                else:
                    self.curr_child.left = new_node

                self.curr_child = new_node

            self.curr_direction = 'Left'

            return True
        else:

            if (self.curr_child.decision_var != literal and self.curr_child.text != 'root'):
                new_node = None
                if self.first:
                    new_node = Node('initial UP')
                else:
                    new_node = Node('UP')
                new_node.decision_var = literal
                if (self.curr_direction == 'Right'):
                    self.curr_child.right = new_node
                else:
                    self.curr_child.left = new_node
                self.curr_child = new_node
            self.curr_direction = 'Left'

            self.assignment_stack[-1][abs(literal)] = bsign(literal, True)
            self.propagation_queue.append(literal * -1)

            return True

    def compute_activity_ordering(self) -> List[Var]:
        """Returns a list of variables [1..n] sorted by descending activity score
        based on the stored CNF."""
        cnf = self.cnf
        n = self.n

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

        for i in range(n+1):
            found = False
            for clause in cnf:
                for variable in clause:
                    if variable == i or abs(variable) == i:
                        found = True
            if not found and i in vars:
                vars.remove(i)

        return vars

    def pick_variable(self) -> Optional[Var]:
        """Returns the first unassigned variable in the stored variable ordering,
        or `None` if all variables have been assigned."""

        for i in range(len(self.var_ordering)):
            index = self.var_ordering[i]
            if self.assignment_stack[-1][index] is None:
                new_node = Node('Decision')
                new_node.decision_var = index
                if self.curr_direction == "Right":
                    self.curr_child.right = new_node
                else:
                    self.curr_child.left = new_node

                self.curr_child = new_node
                self.last_decision = new_node

                self.curr_direction = None

                return index
        return None

    def propagate_from(self, false_literal: Lit) -> bool:
        """
        Accepts as input a literal which has been assigned to `False`, and updates the
        watched literals of every clause previously watching that literal in order to
        maintain the 2 Watched Literals invariant, performing unit propagation as needed.

        Returns `False` if a conflict occurs; otherwise `True`.
        """

        for _ in range(len(self.clauses_watching[false_literal])):
            clause = self.clauses_watching[false_literal].popleft()

            if len(clause) == 1:

                return False

            if clause[1] != false_literal:
                clause[0], clause[1] = clause[1], clause[0]
            if self.value(clause[0]) is True:
                self.clauses_watching[false_literal].append(clause)
                continue

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
        """
        Calls `propagate_from()` on every literal in the propagation queue
        until the queue is empty. If we ever encounter a conflict, this
        returns `False`; otherwise `True`.
        """

        while self.propagation_queue:
            literal = self.propagation_queue.popleft()
            if (self.propagate_from(literal) is False):
                new_node = Node('CONFLICT')
                if self.curr_direction == 'Right':
                    self.curr_child.right = new_node
                else:
                    self.curr_child.left = new_node
                self.curr_child = new_node

                return False

            if (self.curr_child.decision_var != literal):
                new_node = None
                if self.first:
                    new_node = Node('initial UP')
                else:
                    new_node = Node('UP')
                new_node.decision_var = literal
                if self.curr_direction == 'Right':
                    self.curr_child.right = new_node
                else:
                    self.curr_child.left = new_node

            if self.value(literal) is False:
                self.curr_direction = 'Right'
            elif self.value(literal) is True:
                self.curr_direction = 'Left'

            self.curr_child = new_node

        return True

    def backtrack_and_assume_negation(self) -> None:
        """Undo the last decision and restore the previous partial assignment.
        Then assume the negation of the last decision variable."""

        self.assignment_stack.pop()
        self.propagation_queue = deque()
        if not self.decision_stack:
            return
        last_decision = self.decision_stack.pop()
        self.assume(-1 * last_decision)

        if self.curr_direction == 'Right':
            self.curr_direction == 'Left'
        elif self.curr_direction == 'Left':
            self.curr_direction == 'Right'

        if self.last_decision.right is not None:
            self.curr_direction = 'Left'
        elif self.last_decision.left is not None:
            self.curr_direction = 'Right'

        self.curr_child = self.last_decision

        return

    def solve(self) -> Union[str, List[Lit]]:
        """Return a satisfying assignment to the stored CNF, or return `'UNSAT'` if none exists."""

        if self.next == 1:

            for clause in self.cnf:
                if len(clause) == 1:

                    if self.assume(clause[0]) is False:
                        return "UNSAT"

                    if (self.curr_child.decision_var != clause[0]):
                        new_node = None
                        if self.first:
                            new_node = Node('initial UP')
                        else:
                            new_node = Node('UP')
                        new_node.decision_var = clause[0]
                        if self.curr_direction == 'Right':
                            self.curr_child.right = new_node
                        else:
                            self.curr_child.left = new_node

                        if self.value(clause[0]) is False:
                            self.curr_direction = 'Right'
                        elif self.value(clause[0]) is True:
                            self.curr_direction = 'Left'
                        self.curr_child = new_node

            self.switch = -1
            self.next = 2
            self.first = False

        if self.next == 2:
            if not self.unit_propagate():
                return 'UNSAT'
            self.switch = -1
            self.next = 3
            self.check_all_set = True
            return 'image1'

        if self.check_all_set:
            self.check_all_set = False
            local_sat = self.assignment_stack[-1]

            for index, var in enumerate(local_sat):

                if index != 0 and var is None and index in self.var_ordering:

                    break
            else:
                self.sat = [lit(x, self.value(x))
                            for x in range(1, self.n + 1)]
                return 'SAT'
            return 'image3'

        if self.next == 3:
            if (self.switch == 1):
                self.switch = -1

                return 'image4'

            while True:
                if self.in_loop == 1:
                    self.decision = self.pick_variable()
                    if self.decision is None:

                        self.check_all_set = True

                        return 'image2'
                        break

                    self.decision_stack.append(self.decision)
                    new_assignment = self.assignment_stack[-1].copy()

                    self.assignment_stack.append(new_assignment)
                    self.in_loop = 2
                    self.switch = -1

                if self.in_loop == 2:
                    self.assume(self.decision)
                    self.in_loop = 3
                    self.switch = -1

                    if not (self.skip_this):
                        self.skip_this = True
                        return 'image4'

                if self.in_loop == 3:

                    if not self.check_unit_prop:

                        if not self.unit_propagate():
                            self.check_unit_prop = True
                            return 'image5'
                        else:
                            self.in_loop = 1
                            self.check_all_set = True
                            self.skip_this = False
                            return 'image2'

                    else:
                        if not self.check_level_0:

                            self.check_level_0 = True
                            if len(self.assignment_stack) == 1:
                                return 'UNSAT'
                            else:

                                return 'image6'
                        else:
                            self.check_level_0 = False

                            self.in_loop = 2

                            self.check_unit_prop = False

                            self.backtrack_and_assume_negation()

                            return 'image4'

            self.sat = [lit(x, self.value(x)) for x in range(1, self.n + 1)]
            return "SAT"

    def start(self):
        for clause in self.cnf:
            if len(clause) == 1:
                if self.assume(clause[0]) is False:
                    return "UNSAT"
        return "not yet"
