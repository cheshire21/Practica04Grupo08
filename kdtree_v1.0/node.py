
class Node:
  def __init__(self,point,axis):
    self.point=point
    self.axis=axis
    self.left=None
    self.right=None
    self.label=None
  def get_position(self):
    # return position tuple
    return self.point

  def get_children(self):
    # return childen Node tuple
    return (self.left,self.right)