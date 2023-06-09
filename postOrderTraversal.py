
'''
Given the root of a binary tree, return the postorder traversal of its nodes' values.
'''

#just an optimal solution iterative
class Solution(object):
    def postorderTraversal(self, root):
        result = []
        stack = [(root, "visit")]

        while stack:
            curr_node, action = stack.pop()
            if curr_node:
                if action == "visit":
                    result.append(curr_node.val)
                    stack.append((curr_node, "done"))
                    stack.append((curr_node.left, "visit"))
                    stack.append((curr_node.right, "visit"))
                elif action == "done":
                    continue

        return result[::-1]
      
      
    #best timer 3ms
class Solution(object):
    def postorderTraversal(self, root):
        
        def po(node, po_list):
            if node:
                po(node.left, po_list)
                po(node.right, po_list)
                po_list.append(node.val)
                
        po_list = []
        po(root, po_list)
        return po_list
      
      
  #best memory usage 13000kb
  class Solution(object):
    def postorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        result = []
        if root:
            result = result + self.postorderTraversal(root.left)
            result = result + self.postorderTraversal(root.right)
            result.append(root.val)
        return result
