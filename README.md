# cis189FinalProject

### Overview of completed work
For our final project, we made a PennSAT visualizer designed to take in relatively simple CNFs in order to clarify the DPLL algorithm for future learners. We created a GUI that a user can run to input a CNF, and then run the algorithm processively by pressing the next button until PennSAT has found that the CNF is satisfiable or unsatisfiable. When the next button is pressed, the GUI will display the current state of the algorithm as several components: the assignment stack, a list of the clauses each variable watching a clause is watching, and a tree representation of variables that the algorithm has assumed. We also included the same flowchart from lecture/the homework assignment and at each step of the algorithm, the flowchart will indicate which step of the algorithm it is on.

### Overview of the file structure / explanation of what each file contains

- `gui.py` - the first screen where you can enter your own CNF or you can use a randomized CNF
- `solver_phase.py` - shows the second screen with the sections for each display
-  `tree.py` - functions that take in parameters from solver_phase and draws a tree based on solely the parameters it receives
- `iterative_pennSAT.py` - A modified version of the file from homework2. This version has many new internal variables including the decision tree, various casing variables, and more. It returns either "SAT," "UNSAT," or "image[x]" depending on what it should display on the screen and the state of the solver
- `images/` - JPG versions of the flowchart, each version with a different box highlighted

#### Installation:
- Download [Python3](https://www.python.org/downloads/)

- Install Pillow
    ```sh
    $ python3 -m pip install Pillow
    ```
    or 
    ```sh
    $ py -3 -m pip install Pillow
    ```

#### To Run:
```sh
$ python3 gui.py
```
or 
```sh
$ py -3 gui.py
```

