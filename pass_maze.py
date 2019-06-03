import random
import time
import copy
import math


inform = True
algorithm = 'bfs'
filename = 'mediumMaze.txt'
start_time = time.time()
with open(filename, 'r', encoding='utf8') as f:
    datas = f.readlines()
    datas = list(map(lambda x: list(x), datas))


def txt2list():
    """
    将txt形式的迷宫转换成list
    :return:
    maze: 列表形式的迷宫
    start: 迷宫的初时位置
    end: 迷宫所在的终点
    """
    maze = list()
    for p, i in enumerate(datas):
        i = i[:-1]
        single_line = []
        for q, j in enumerate(i):
            if j == '%':
                single_line.append(1)
            elif j == ' ':
                single_line.append(0)
            elif j == 'P':
                single_line.append(1)
                start = (p, q, 1)
            elif j == '.':
                single_line.append(-2)
                end = (p, q)
        maze.append(single_line)
    return maze, start, end


def search(now_maze, position):
    """
    从当前位置到下一个分岔口
    :param now_maze: 记录走过的路径的迷宫
    :param position: 当前位置
    :return:
    judge：判断是否抵达终点
    now_maze: 结束后更新的迷宫状态
    flag: 叉入口有几条路
    """
    x, y, step = position
    flag = 1
    new_knots = []
    if now_maze[x][y] > 1:
        return False, now_maze, [], 0
    while (flag == 1):
        flag = 0
        now_maze[x][y] = step
        steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for i, j in steps:
            if now_maze[x + i][y + j] == -2:
                return True, now_maze, [], (x, y, now_maze[x][y])
            if now_maze[x + i][y + j] == 0:
                flag = flag + 1
                step = now_maze[x][y] + 1
                new_knots.append((x + i, y + j, step))
        if flag == 1:
            x, y, step = new_knots.pop(0)
    # show(now_maze)
    return False, now_maze, new_knots, flag


def show(maze):
    """
    打印当前迷宫状态
    :param maze: 当前迷宫
    :return:
    """
    for i in maze:
        for j in i:
            print('%(j)3s' % {'j': str(j)}, end=' ')
        print()
    print()


def blindsearch(maze, start, dfs=0):
    """
    通过深度优先搜索或广度优先搜索寻找迷宫路径
    :param maze: 迷宫
    :param start: 开始位置
    :param dfs: 是否是深度优先搜索
    :return:
    """
    stack = list()
    stack.append(start)
    now_maze = copy.deepcopy(maze)
    count_knot = 0
    while len(stack) > 0:
        position = stack.pop(-dfs)
        judge, now_maze, new_knots, flag = search(now_maze, position)
        count_knot = count_knot + 1
        random.shuffle(new_knots)
        for i in new_knots:
            if i not in stack:
                stack.append(i)
        if judge == True:
            list2txt(datas, now_maze, flag, count_knot)
            return


def list2txt(maze, now_maze, end, count_knot):
    """
    将运行结果记录在txt文本中
    :param maze: 原始的迷宫状态图
    :param now_maze: 探索过的迷宫
    :param end: 抵达终点前一刻的位置
    :param count_knot: 搜索过的结点数
    :return:
    """
    global start_time
    x, y, step = end
    final_step = step
    while step > 1:
        maze[x][y] = '0'
        steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for i, j in steps:
            if now_maze[x+i][y+j] == step - 1:
                step = step - 1
                x = x + i
                y = y + j
                break
    with open('results/' + filename + algorithm + str(time.time()) + '.txt', 'w', encoding='utf8') as f:
        for i in maze:
            f.writelines(i)
            f.writelines('')
        f.writelines(['\n搜索结点数：' + str(count_knot)])
        f.writelines(['\n步骤数：' + str(final_step)])
        f.writelines(['\n运行时间：' + str(time.time() - start_time)])


def best_first(now_postion, end):
    """
    最好优先搜索的启发函数
    :param now_postion:当前的位置
    :param end:
    :return:
    distance：当前位置与目标位置的估计代价
    """
    global algorithm
    algorithm = ' best_first'
    x, y, _ = now_postion
    p, q = end
    return abs(x-p) + abs(y-q)


def a_star_weighted(now_postion, end, i):
    global algorithm
    algorithm = ' a_star ' + str(i)
    x, y, step = now_postion
    p, q = end
    return i*(abs(x-p) + abs(y-q)) + (1-i)*step


def mul_sqrt(now_postion, end):
    global algorithm
    algorithm = ' mul_sqrt'
    x, y, step = now_postion
    p, q = end
    return (abs(x - p) + abs(y - q)) * step

def a_star(now_postion, end):
    global algorithm
    algorithm = ' a_star'
    x, y, step = now_postion
    p, q = end
    return abs(x-p) + abs(y-q) + step


def dijkstra(now_postion, end):
    global algorithm
    algorithm = ' dijkstra'
    x, y, step = now_postion
    p, q = end
    return step

def close_a(now_postion, end):
    global algorithm
    algorithm = ' close_a'
    x, y, step = now_postion
    p, q = end
    return (math.sqrt(abs(x-p) + abs(y-q)) + math.sqrt(step))**2

def inform_search(maze, start, end, f, iss):
    stack = list()
    stack.append(start)
    now_maze = copy.deepcopy(maze)
    count_knot = 0
    while len(stack) > 0:
        position = stack.pop(0)
        judge, now_maze, new_knots, flag = search(now_maze, position)
        count_knot = count_knot + 1
        stack.extend(new_knots)
        stack.sort(key=lambda x: f(x, end))
        if judge == True:
            list2txt(datas, now_maze, flag, count_knot)
            return



if __name__ == '__main__':
    maze, start, end = txt2list()
    if inform == False:
        if algorithm == 'dfs':
            dfs = 1
        elif algorithm == 'bfs':
            dfs = 0
        blindsearch(maze, start, dfs=dfs)
    else:
        inform_search(maze, start, end, a_star_weighted)
