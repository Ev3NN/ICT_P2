# Q1 - Huffman Coding in python
# Source: https://www.programiz.com/dsa/huffman-coding
class NodeTree(object):
    """
    A class used to represent a node of a binary tree.
    """

    def __init__(self, left=None, right=None):
        """
        Parameters
        ----------
        left : str
            The label of the left child
        right : str
            The label of the right child
        """
        self.left = left
        self.right = right

    def children(self):
        """
        Returns the children of the node (i.e., left child and right child)
        """
        return (self.left, self.right)

    def __str__(self):
        "Returns the node converted into a string"
        return '%s_%s' % (self.left, self.right)

def huffman_code_tree(node, binString=''):
    """
    Returns the huffman code given a huffman tree

    Parameters
    ----------
    node: NodeTree
        The root node of the huffman tree
    binString : str
        The encoded string of the node
    """
    if type(node) is str:
        return {node: binString}

    (l, r) = node.children()
    d = dict()

    d.update(huffman_code_tree(l, binString + '0'))
    d.update(huffman_code_tree(r, binString + '1'))

    return d

def build_tree(nodes):
    """
    Returns the built huffman tree

    Parameters
    ----------
    nodes: list
        A list of tuples (key, c) representing the probability
        distribution, where key is the label and c is the value.
    """
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]

        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    return nodes

def main():
    # Data from ex 7: https://people.montefiore.uliege.be/asutera/ict_tp/tp2_2020-2021.pdf
    freq = {'A': 0.05, 'B': 0.1, 'C': 0.15, 'D': 0.15, 'E': 0.2, 'F': 0.35}
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    nodes = build_tree(freq)
    huffmanCode = huffman_code_tree(nodes[0][0])
    
    print(' Char | Huffman code ')
    print('----------------------')
    for (char, _) in freq:
        print(' %-4r |%12s' % (char, huffmanCode[char]))

if __name__ == "__main__":
    main()