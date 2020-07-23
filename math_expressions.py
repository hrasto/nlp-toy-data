import numpy as np

def num2word(x):
    nums = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    word = nums[0]
    sign = "minus " if x < 0 else ""
    x = round(abs(x), 2)
    dec = int((x*100)%100)
    dec_verbal = ''
    if dec > 9:
        dec_verbal = ' point {}'.format(num2word(dec))
    elif dec > 0:
        dec_verbal = ' point {} {}'.format(nums[0], nums[dec])
    x = int(x)
    ones = int(x) % 10
    if ones > 0: word = nums[ones]
    tens = (x % 100) // 10
    ties = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    teens = ['ten', 'eleven', 'twelve', 'thirteen', 'forteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    if tens > 1:
        word = ties[tens-2] + '-' + word if ones > 0 else ties[tens-2]
    if tens == 1:
        word = teens[ones]
    hundreds = int(x % 1e3 // 1e2)
    if hundreds > 0:
        word = nums[hundreds] + ' hundred' + (' and ' + word if ones + tens > 0 else '')
    thousands = int(x % 1e6 // 1e3)
    if thousands > 0:
        word = num2word(thousands) + ' thousand' + ((' and ' if hundreds==0 else ' ') + word if ones + tens + hundreds > 0 else '')
    millions = int(x % 1e9 // 1e6)
    if millions > 0:
        word = num2word(millions) + ' million' + ((' and ' if hundreds+thousands==0 else ' ') + word if ones + tens + hundreds + thousands > 0 else '')
    billions = int(x % 1e12 // 1e9)
    if billions > 0:
        word = num2word(billions) + ' billion' + ((' and ' if hundreds+thousands+millions==0 else ' ') + word if ones + tens + hundreds + thousands + millions > 0 else '')

    return sign+word+dec_verbal

class Queue:
    def __init__(self, N):
        self.ls = []
        self.N = N
    def enqueue(self, x):
        self.ls.insert(0, x)
        if len(self.ls) > self.N: self.ls.pop()

class OpNode:
    def __init__(self, lop, rop):
        self.lop = lop # left operand
        self.rop = rop # right operand
    def compute(self):
        pass
    def to_word(self):
        return num2word(self.compute())
    def helper_nth_num_apply(self, func, n=1):
        """
        Provides access to the nth recursively found Number instance of this node.
        If 0 was not returned, there isn't an nth Number instance.
        """
        if isinstance(self, Number):
            if n == 1:
                #print("Applying func to ", self.val)
                self.val = func(self.val)
                #print("modified value is ", self.val)
            return n-1
        else:
            new_n = self.rop.helper_nth_num_apply(func, n)
            if not new_n == 0:
                new_n = self.lop.helper_nth_num_apply(func, new_n)
            return new_n

class Number(OpNode):
    def __init__(self, num):
        self.val = num
    def compute(self):
        return self.val
    def __str__(self):
        return '('+str(self.val)+')' if self.val < 0 else str(self.val)

class AddNode(OpNode):
    def compute(self):
        return self.lop.compute() + self.rop.compute()
    def __str__(self):
        return '('+str(self.lop)+'+'+str(self.rop)+')'

class SubtractNode(OpNode):
    def compute(self):
        return self.lop.compute() - self.rop.compute()
    def __str__(self):
        return '('+str(self.lop)+'-'+str(self.rop)+')'

class MultiplyNode(OpNode):
    def compute(self):
        return self.lop.compute() * self.rop.compute()
    def __str__(self):
        return '('+str(self.lop)+'*'+str(self.rop)+')'

class DivideNode(OpNode):
    def __init__(self, lop, rop):
        n = 1
        while rop.compute() == 0:
            rop.helper_nth_num_apply(lambda x: x+1, n)
            n += 1
        assert not rop.compute() == 0, 'Cannot divide with 0 :('
        super().__init__(lop, rop)
    def compute(self):
        return self.lop.compute() / self.rop.compute()
    def __str__(self):
        return '('+str(self.lop)+'/'+str(self.rop)+')'

class PowerNode(OpNode):
    def __init__(self, lop, rop):
        # here we need to recursively decrease magnitudes of all the rop-children
        # otherwise the value might explode :O
        def helper(node: OpNode):
            if isinstance(node, Number):
                node.val = (int(np.random.uniform(0, 8))/2-2)
            elif not isinstance(node, PowerNode):
                if not isinstance(node.lop, PowerNode): helper(node.lop)
                # if node is a division, let it be because it has to stay non-zero
                if not (isinstance(node.rop, PowerNode) or isinstance(node, DivideNode)):
                    helper(node.rop)
        helper(rop)
        rop_res = rop.compute()
        assert not isinstance(rop_res, complex)
        if not rop_res.is_integer():
            n = 1
            while lop.compute()<0:
                lop.helper_nth_num_apply(lambda x: x*(-1), n)
                n += 1
                if n == 10: break # stay safe
        super().__init__(lop, rop)
    def compute(self):
        return self.lop.compute() ** self.rop.compute()
    def __str__(self):
        return '('+str(self.lop)+'**('+str(self.rop)+'))'

def binary_tree_generator(n=4):
    """
    Creates representation for a randomly created binary tree with no balancing.
    (https://stackoverflow.com/questions/47307915/python-generate-a-random-binary-tree-with-n-vertices)
    """
    # start with root node and no children
    tree = [[-1, -1]]
    free_edges = [(0, 0), (0, 1)]
    while len(tree) < n:
        e = free_edges[np.random.randint(0, len(free_edges))]  # select a free edge
        node, child = e
        assert tree[node][child] == -1  # make sure we made no mistake
        k = len(tree)  # index of new node
        tree.append([-1, -1])  # add new node
        tree[node][child] = k  # set new node as child of an old node
        free_edges.extend([(k, 0), (k, 1)])  # new node has two free edges
        free_edges.remove(e)  # edge is no longer free
    return tree

def recursive_tree_transform(
    rootnode,
    tree,
    dist=np.random.uniform,
    num_range=(-10,10),
    node_types = [AddNode, SubtractNode, MultiplyNode, DivideNode, PowerNode]
):
    """
    Recursively traverses the given tree starting from the rootnode.
    Operands are initialized from the bottom up,
    so all the children of a node are already accessible from the operand's __init__ function.
    Meant to use after creating a binary tree representation with 'binary_tree_generator'.
    """
    num_min, num_max = num_range
    assert num_min < num_max
    return node_types[np.random.randint(0,len(node_types))](
        Number(int(dist(num_min,num_max)*100)/100) if rootnode[0]==-1 else recursive_tree_transform(tree[rootnode[0]], tree),
        Number(int(dist(num_min,num_max)*100)/100) if rootnode[1]==-1 else recursive_tree_transform(tree[rootnode[1]], tree)
    )

def generate_nested_expression(
    num_range=(-10, 10),
    depth=4,
    dist=np.random.uniform,
    ops=[AddNode, SubtractNode, MultiplyNode, DivideNode, PowerNode]
):
    """
    Generates a nested mathematical expression with parantheses containing 'depth' nodes (operations).
    """
    tree = binary_tree_generator(depth)
    root = recursive_tree_transform(tree[0], tree, dist, num_range, ops)
    #print(root.compute())
    #print(eval(str(root)))
    return root

def nested_expression_robustness_test(N=100):
    for i in range(N):
        try:
            root = generate_nested_expression()
            res = root.compute()
            if isinstance(res, complex): raise "{}: Complex result not allowed".format(str(root) )
            if abs(res-eval(str(root))) > 1e-3: raise "{}: eval() returns {} while tree computes {}".format(str(root), eval(str(root)), res)
        except:
            print("Failed due to an exception. Stopping at {} expressions.".format(i))
            raise
    print("Test passed with {} iterations!".format(N))

def generate_simple_expression(num_range=(-10, 10), len_range = (4, 12), dist=np.random.uniform, verbal=False):
    """
    Generates a simple sequential mathematical expression only containing +,-,*,and / operations.
    """
    op_src = ['+', '-', '*', '/']
    op_tg = ['plus', 'minus', 'times', 'divided by']
    min_num, max_num = num_range
    min_len, max_len = len_range
    assert min_len < max_len and min_len > 0
    seq_len = np.random.randint(min_len, max_len)
    seq_nums = dist(min_num, max_num, seq_len).astype(np.int)
    seq_ops = np.random.uniform(0, len(op_src), seq_len-1).astype(np.int)
    sent = ''
    for i in range(seq_len):
        if i>0:
            sent += ' '+(op_tg[seq_ops[i-1]] if verbal else op_src[seq_ops[i-1]])+' '
        sent += num2word(seq_nums[i]) if verbal else str(seq_nums[i])
    return sent
