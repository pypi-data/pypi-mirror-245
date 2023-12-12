import os

code_block_networkx = """import networkx as nx

def pagerank(G, alpha=0.85, tol=1.0e-6, max_iter=100):
    n = len(G)
    pr = {node: 1.0 / n for node in G}

    for _ in range(max_iter):
        delta = 0.0
        for node in G:
            in_neighbors = G.predecessors(node)
            new_pr = (1 - alpha) + alpha * sum(pr[in_neighbor] / G.out_degree(in_neighbor) for in_neighbor in in_neighbors)
            delta += abs(new_pr - pr[node])
            pr[node] = new_pr

        if delta < n * tol:
            break

    return pr

# Example usage
G = nx.DiGraph()
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'A')])

print(pagerank(G))
"""
def getcodepr():
# Get the current working directory
    current_directory = os.getcwd()

# Specify the file path
    file_path_networkx = os.path.join(current_directory, "example_networkx_code.py")

# Open the file in write mode and write the content
    with open(file_path_networkx, "w") as file:
        file.write(code_block_networkx)

    print(f"NetworkX code block saved at: {file_path_networkx}")
