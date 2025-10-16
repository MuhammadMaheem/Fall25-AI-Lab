# # # # # string1 = "Kuch,Bhi:Kuch?Bhi!"

# # # # # not_allowed = set("~`!@#$%^&*()_+-={}[]|\:;'\"<>?/,.")


# # # # # for i in string1:
# # # # #     if i in not_allowed:
# # # # #         string1 = string1.replace(i , " ")
# # # # #     print(string1)

















# # # # # # sort teh string


# # # # # string1 = "I am Rasikh"
# # # # # x = []
# # # # # x = [ord(ch) for ch in string1 ]
# # # # # print(x)
# # # # # for i in range(len(x)):
# # # # #     secd = x[i]  
# # # # #     for j in range(i+1, len(x)):   
# # # # #         if x[j] < secd:
# # # # #             print(x[j], "<", secd)





# # # # string1 = "I am Rasikh"
# # # # x = [ord(ch) for ch in string1]

# # # # sorted_list = []
# # # # for val in x:  
# # # #     count = 0
# # # #     while count < len(sorted_list) and sorted_list[count] <val:
# # # #         count +=1
# # # #         print(count)

# # # #     sorted_list.insert(count,val)
# # # #     print(sorted_list)


# # # # assi_code = [chr(ch) for (ch) in sorted_list]
# # # # print(assi_code)








# # # # # card_num = input("Enter your card number: ")
# # # # # sum1 = 0
# # # # # for i in range(len(card_num)-1, -1, -1):
# # # # #     print(i)
# # # # #     digit = int(card_num[i])
# # # # #     print(digit)
# # # # #     if (len(card_num) - i) % 2 == 0:
# # # # #         digit *= 2
# # # # #         if digit > 9:
# # # # #             digit -= 9
# # # # #     sum1 += digit
# # # # # if sum1 % 10 == 0:
# # # # #     print("Valid card number")
# # # # # else:
# # # # #     print("Invalid card number")





# # # # card_num = list(input("Enter your card number: "))
# # # # sum1 = 0
# # # # last_digit = card_num.pop()
# # # # print(last_digit)
# # # # print(card_num)
# # # # reversed_num = card_num[::-1]
# # # # print(reversed_num)
# # # # new_list = []
# # # # for i in range(len(reversed_num)):
# # # #     if i % 2 == 0:
# # # #         new_list.append(int(reversed_num[i]) * 2)
# # # #     else:
# # # #         new_list.append(int(reversed_num[i]))
# # # # print(new_list)
# # # # for i in new_list:
# # # #     if i > 9:
# # # #         i -= 9
# # # #     sum1 += i
# # # # print(sum1)
# # # # sum1 += int(last_digit)
# # # # if sum1 % 10 == 0:
# # # #     print("Valid card number")
# # # # else:
# # # #     print("Invalid card number")
















# # # tree = {
# # #     0: [1, 2],
# # #     1: [3, 4],
# # #     2: [5],
# # #     3: [],
# # #     4: [],
# # #     5: []
# # # }

# # # start = 0

# # # visited = set()
# # # stack = [start]

# # # result = []

# # # while stack:
# # #     i = stack.pop()
    
# # #     if i not in visited:
# # #         visited.add(i)
# # #         result.append(i)
        
# # #         for j in reversed(tree[i]):
# # #             if j not in visited:
# # #                 stack.append(j)

# # # print(result)

















# # #            #  0
# # # #           /   \
# # # #          1     2
# # # #         / \     \
# # # #        3   4     5
# # # #             \     \
# # # #              6     7





# # # count = 0

# # # def dfs(graph, start, limit, visited=None):
# # #     global count
    
# # #     if visited is None:
# # #         visited = set()
    
# # #     if count >= limit: 
# # #         return visited
        
# # #     visited.add(start)
# # #     print(start)
# # #     count += 1
    
# # #     if count >= limit:  
# # #         return visited
    
# # #     for next_node in graph[start] - visited:
# # #         dfs(graph, next_node, limit, visited)
# # #         if count >= limit: 
# # #             break
    
# # #     return visited

# # # graph = {'0': set(['1', '2']),
# # #          '1': set(['0', '3', '4']),
# # #          '2': set(['0']),
# # #          '3': set(['1']),
# # #          '4': set(['2', '3'])}

# # # count = 0


# # # dfs(graph, '0',4)


# # # #        0
# # # #       / \
# # # #      1   2
# # # #     / \
# # # #    3   4














# # # # def print_levels(tree, node, level=1):
# # # #     children = tree.get(node, [])
    
# # # #     if not children:
# # # #         print(f"Node {node}: No level")
# # # #     else:
# # # #         print(f"Node {node}: Level {level}")
# # # #         for child in children:
# # # #             print_levels(tree, child, level + 1)

# # # tree = {
# # #     0: [1, 2],
# # #     1: [3, 4],
# # #     2: [5],
# # #     3: [],
# # #     4: [6],
# # #     5: [7]
# # # }

# # # # print_levels(tree, 0)






# # tree = {
# #     0: [1, 2],
# #     1: [3, 4],
# #     2: [5],
# #     3: [],
# #     4: [],
# #     5: [6],
# #     6: []
# # }



# # def dls(start, target, depth_limit):
# #     stack = [(start, 0)] 
# #     visited_order = []

# #     while stack:
# #         node, depth = stack.pop(0)  
# #         visited_order.append(node)

# #         if node == target:
# #             return True, visited_order

# #         if depth < depth_limit and node in tree:
# #             for child in tree[node]:
# #                 stack.append((child, depth + 1))

# #     return False, visited_order


# # limit = len(tree) // 2

# # found, visited = dls(start=0, target=4, depth_limit=limit)

# # print(visited)


# # # length = len(tree )//2
# # # print(length)



# # # for i in range(length):
# # #     if i in tree:
    






# # #     0
# # #    / \
# # #   1   2
# # #  / \     \
# # # 3   4     5
# # #             \   
# # #               6   















# # wanted_nodes = {'A', 'B', 'C', 'F'}

# # def dls(graph, start, limit, visited=None, depth=0):
# #     if visited is None:
# #         visited = set()

# #     visited.add(start)

# #     if depth <= limit and start in wanted_nodes:
# #         print(f"{start} (depth {depth})")

# #     if depth == limit:
# #         return visited

# #     for next in sorted(graph.get(start, [])):
# #         if next not in visited:
# #             dls(graph, next, limit, visited, depth + 1)

# #     return visited


# # graph = {
# #     'A': {'C',},
# #     'B': {'D', 'E'},
# #     'C': {'F'},
# #     'D': set(),
# #     'E': set(),
# #     'F': {'G'},
# #     'G': set()
# # }
# # visited_nodes = dls(graph, 'A', limit=2)
# # print("\nVisited set:", visited_nodes)


# from collections import deque

# def bfs_until_target(graph, start, target, limit):
#     queue = deque([(start, 0, [start])])  # (node, depth, path)
#     visited = {start}
#     visit_order = [start]
#     print(f"{start} (depth 0)")

#     if start == target:
#         return [start], visit_order

#     while queue:
#         node, depth, path = queue.popleft()

#         if depth >= limit:
#             continue

#         for nb in sorted(graph.get(node, [])):
#             if nb not in visited:
#                 visited.add(nb)
#                 visit_order.append(nb)
#                 print(f"{nb} (depth {depth + 1})")

#                 if nb == target:
#                     return path + [nb], visit_order

#                 queue.append((nb, depth + 1, path + [nb]))

#     return None, visit_order


# graph = {
#     'A': {'B', 'C'},
#     'B': {'D', 'E'},
#     'C': {'F'},
#     'D': set(),
#     'E': set(),
#     'F': {'G'},
#     'G': set()
# }

# path, order = bfs_until_target(graph, 'A', 'F', limit=2)
# print("\nVisit order:", order)
# print("Path to F:", path)

















graph = { 
    'A': {'B', 'C'},
    'B': {'C', 'D', 'E'},
    'C': {'F'},
    'D': set(),
    'E': set(),
    'F': {'G'},
    'G': set()
} 

def dls(start, goal, path, level, max_depth):
    print(f"Level: {level}, Current node: {start}")
    path.append(start)
    
    if start == goal:
        return True
    
    if level == max_depth:
        path.pop()
        return False
    

    for child in sorted(graph[start]):
        if dls(child, goal, path, level + 1, max_depth):
            return True
    
    path.pop()
    return False

start = 'A'
goal = input("Enter the goal state: ").upper()
max_depth = int(input("Enter the limit: "))
path = []

found = dls(start, goal, path, 0, max_depth)

if found:
    result = ''.join(path)
    print(f"Path found: {result}")
    print(f"Path length: {len(result)}")
else:
    print("Path not found within depth limit")
    if path:
        result = ''.join(path)
        print(f"Deepest path explored: {result}")
        print(f"Path length: {len(result)}")