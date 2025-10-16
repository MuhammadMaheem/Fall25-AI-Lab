# # graph = {
# #     'A': ['B', 'C'],
# #     'B': ['D', 'E'],
# #     'C': ['F'],
# #     'D': ['G', 'H'],
# #     'E': [],
# #     'F': ['I', 'K'],
# #     'G': [],
# #     'H': ['L'],
# #     'I': [],
   
# # }

# # def bfs(start, end):
# #     queue = [[start]]  
# #     visited = set()   

# #     while queue:
# #         path = queue.pop(0)       
# #         node = path[-1]          


# #         if node == end:
# #             return path            

# #         if node not in visited:
# #             visited.add(node)
# #             for child in graph[node]:
# #                 new_path = path + [child]
# #                 queue.append(new_path)

# #     return False


# # start = 'A'
# # end = input("Targets: ").upper()
    
# # taget = bfs(start, end)
# # print("Path", taget)


















# # def bfs_with_target_and_visited(graph, start, target):
# #     visited = set()          
# #     current_level = [start]  
# #     traversal_order = []   

# #     while current_level:
# #         next_level = []      
# #         for node in current_level:
# #             if node not in visited:
# #                 print(f"Visiting: {node}")  
# #                 traversal_order.append(node)
                
# #                 if node == target:  
# #                     print(f"Found target: {target}!")
# #                     print(f"Visited nodes: {list(visited) + [node]}")
# #                     print(f"Traversal order: {traversal_order}")
# #                     return f"Success: Found {target}!"
                
# #                 visited.add(node)  
                
# #                 for neighbor in graph[node]:
# #                     if neighbor not in visited:
# #                         next_level.append(neighbor)
        
# #         current_level = next_level
    
# #     print(f"Visited nodes: {visited}")
# #     return f"Target {target} not found"

# # graph = {
# #     'A': ['B', 'C'],
# #     'B': ['D', 'E'],
# #     'C': ['F'],
# #     'D': [],
# #     'E': ['F'],
# #     'F': []
# # }

# # print(bfs_with_target_and_visited(graph, 'A', 'E'))





















# def bfs(root):
#     if not root:
#         return
    
#     queue = [root]  # Use simple list instead of deque
    
#     while queue:
#         node = queue[0]           # Get first element (like popleft)
#         print(node.val)           # Process node
#         queue = queue[1:]         # Remove first element (like popleft)
        
#         # Add children to end of queue
#         if node.left:
#             queue.append(node.left)
#         if node.right:
#             queue.append(node.right)

# # Tree Node class
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# # Create tree: A(B(D,E),C(F))
# root = TreeNode('A')
# root.left = TreeNode('B')
# root.right = TreeNode('C')
# root.left.left = TreeNode('D')
# root.left.right = TreeNode('E')
# root.right.right = TreeNode('F')

# bfs(root)  # Output: A B C D E F










def bfs_visited(graph, start, target):
    visited = set()          
    current_level = [start]  
    traversal_order = []

    while current_level:
        next_level = []      
        for node in current_level:
            if node not in visited:
                print(f"Visiting: {node}")  
                traversal_order.append(node)
                
                if node == target:
                    print(f"Found target: {target}!")
                    print(f"Visited nodes: {list(visited) + [node]}")
                    print(f"Traversal order: {traversal_order}")
                    return f"Success: Found {target}!"
                
                visited.add(node) 
                
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        next_level.append(neighbor)
        
        current_level = next_level
    
    print(f"visited: {visited}")
    return f"Target {target} not found"

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],    
    'E': ['G'],
    'G': ['F']
}

print(bfs_visited(graph, 'A', 'F'))





def bfs_queue(graph, start, target):
    visited = set()
    queue = [start]
    
    while queue:
        node = queue[0]        
        queue = queue[1:]     
        
        print(f"{node}")
        
        if node == target:
            print(f"trget: {target}!")
            return f"Found {target}!"
        
        if node not in visited:
            visited.add(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)  
    print(f" {target}")
    return f"{target}"
print(bfs_queue(graph, 'A', 'F'))
