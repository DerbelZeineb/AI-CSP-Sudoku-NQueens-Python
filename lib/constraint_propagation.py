from __future__ import generators
import time

def AC3(self, X=None, removals=None):

    if X == None:
        queue = [(Xi, Xj) for Xi in self.variables for Xj in self.neighbors[Xi]]
    else:
        queue = [(X, Xj) for Xj in self.neighbors[X] if len(self.domains[Xj]) > 1]

    while len(queue):
        (Xi, Xj) = queue.pop()
        if revise(self, Xi, Xj, removals):
            if len(self.domains[Xi]) == 0: return False
            for Xk in self.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True


def revise(self, Xi, Xj, removals):
    """Return true if we remove a value."""
    revised = False
    for x in self.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not self.constraints(Xi, x, Xj, y) for y in self.curr_domains[Xj]):
            self.prune(Xi, x, removals)
            revised = True
    return revised


def implementAC3(e, pr=True):
    counter = 0
    start_time = time.time()
    elast = dict()
    done = False
    while True:
        check = False
        AC3(e);
        counter += 1
        for i in range(80):
            if i not in e.infer_assignment():
                check = True
                break
        if counter != 0 and check:
            if elast == e.infer_assignment():
                t = time.time() - start_time
                if pr:
                    print()
                    e.display(e.infer_assignment())
                    print('\nSolution not found')
                    print('time taken is %f seconds' % t)
                break
        if not check:
            t = time.time() - start_time
            if pr:
                print()
                e.display(e.infer_assignment())
                print('time taken to solve is %f seconds' % t)
            done = True
            break
        elast = e.infer_assignment().copy()
    return t, done
