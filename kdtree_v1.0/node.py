class Node:
  def __init__(self,point,label,axis):
    self.point=point
    self.axis=axis
    self.left=None
    self.right=None
    self.label=label

  def get_position(self):
    # return position tuple
    return self.point

  def get_label(self):
    # return position tuple
    return self.label

  def get_children(self):
    # return childen Node tuple
    return (self.left,self.right)