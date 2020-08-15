class Node():
    def __init__(self, state, action, sudo):
        self.state = state
        self.action = action
        self.sudo = sudo
    def update(self):
        i, j = self.state
        self.sudo[i][j] = self.action
        return self.sudo

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self, sudo):
        if self.empty():
            print(sudo)
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Maze():
    goal = (8, 8)
    def __init__(self):
        self.solved = []
        self.sudocode = []
    def copy(self, sudocode):
        sudo = {}
        sudo["col"] = [list(x) for x in zip(*sudocode)]
        sudo["row"] = [x[:] for x in sudocode]
        sudo["block"] = []
        for _ in range(9): sudo["block"].append([])
        for i in range(9):
            for j in range(9):
                index = self.det_index(i, j)
                sudo["block"][index].append(sudocode[i][j])
        return sudo

    def addsudo(self):
        incode = [input() for _ in range(9)]
        self.sudocode = list(map(lambda x: [int(y) for y in x], incode))

    def det_index(self, row, col):
        return (row // 3) * 3 + (col // 3)

    def solve(self):
        frontier = StackFrontier()
        sudo = [x[:] for x in self.sudocode]
        i, j = 0, 0
        while True:
            if sudo[i][j] != 0:
                if j < 8:
                    j +=1
                    continue
                i += 1
                j = 0
                continue
            sudodict = self.copy(sudo)
            index = self.det_index(i, j)
            added = False
            for x in range(1, 10):
                if (x not in sudodict["row"][i]) and (x not in sudodict["col"][j]) and (x not in sudodict["block"][index]):
                    node = Node(state = (i, j), action = x, sudo = [x[:] for x in sudo])
                    frontier.add(node)
                    added = True
            node = frontier.remove(sudo)
            sudo = node.update()
            if not added:
                i, j = node.state
            if node.state == self.goal:
                self.solved = sudo
                break

a = Maze()
a.addsudo()
a.solve()
for i in range(9):
    print(a.solved[i])
