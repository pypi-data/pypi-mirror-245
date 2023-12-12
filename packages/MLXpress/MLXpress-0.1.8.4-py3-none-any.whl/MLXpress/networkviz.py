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
cb2= """
class BloomFilter:

    def __init__(self, capacity=100, n=3):
        self.capacity = capacity
        self.filter = [False] * capacity
        self.hashes = [self.hashf(i) for i in range(n)]

    def hashf(self, seed):
        return lambda key: hash((key, seed)) % self.capacity

    def add(self, key):
        for h in self.hashes:
            self.filter[h(key)] = True

    def check(self, key):
        return all(self.filter[h(key)] for h in self.hashes)

# Example usage
bloom_filter = BloomFilter(capacity=100, n=3)
bloom_filter.add("apple")
bloom_filter.add("banana")
print(bloom_filter.check("apple"))  # True
print(bloom_filter.check("orange"))  # False


"""

cb3= """
from apyori import apriori

# Example transactions (list of lists where each list represents a transaction)
transactions = [
    ['bread', 'milk'],
    ['bread', 'diaper', 'beer', 'egg'],
    ['milk', 'diaper', 'beer', 'cola'],
    ['bread', 'milk', 'diaper', 'beer'],
    ['bread', 'milk', 'diaper', 'cola']
]

# Applying Apriori algorithm
result = list(apriori(transactions, min_support=0.3, min_confidence=0.7))

# Displaying the results
for rule in result:
    antecedent = ', '.join(rule.ordered_statistics[0].items_base)
    consequent = ', '.join(rule.ordered_statistics[0].items_add)

    print(f"Rule: {antecedent} -> {consequent}")
    print(f"Support: {rule.support}")
    print(f"Confidence: {rule.ordered_statistics[0].confidence}")
    print("\n")

"""
def getcodepr():
# Get the current working directory
    current_directory = os.getcwd()

# Specify the file path
    fp= os.path.join(current_directory, "pagerank.py")

# Open the file in write mode and write the content
    with open(fp, "w") as file:
        file.write(code_block_networkx)


def getcodebf():
    current_directory = os.getcwd()

    # Specify the file path
    fp2 = os.path.join(current_directory, "bloomfilter.py")

    # Open the file in write mode and write the content
    with open(fp2, "w") as file:
        file.write(cb2)
def getcodeap():
    current_directory = os.getcwd()

    # Specify the file path
    fp3 = os.path.join(current_directory, "apriori.py")

    # Open the file in write mode and write the content
    with open(fp3, "w") as file:
        file.write(cb3)



