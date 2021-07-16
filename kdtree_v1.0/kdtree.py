import pandas as pd
import argparse
import copy
import utils
import numpy as np
from node import Node
from bisect import bisect
import math

class KDTree(object):
  """Construct a kd tree"""
  def __init__(self, file_path):
    """
      Args:
        file_path: a path to a text file that stores points 
    """
    self.pc_path = file_path
    self.dim = 3


    self.points = np.array([[40,70,0],[70,130,0],[90,40,0],
              [110,100,0],
              [140,110,0],
              [160,100,0],
              [150,30,0]
              ])

    self.root = self.build_kdtree_mejorado(self.points, 0)

  def build_kdtree_mejorado(self,points, depth=0):
    n=len(points)
    axis=depth % self.dim
    if(self.dim<=0):
      return None
    if(n==1):
      return Node(points[0],axis)
    median=math.floor(len(points)/2)
    #points.sort(key=(lambda a,b: a[axis]-b[axis]))
    print(points.shape)
    points = points[points[:, axis].argsort(kind='mergesort')]
    
    
    left=points[0:median]
    right=points[median+1:]
    node=Node(points[median],axis)
    node.left=self.build_kdtree_mejorado(left,depth+1)
    node.right=self.build_kdtree_mejorado(right,depth+1)
    return node
  def nearest_neighbor(self, query, curr_node, level):
      
    if curr_node.left is None and curr_node.right is None:
      sqr_dis = np.sum((np.array(query) - curr_node.get_position()) ** 2)
      return [curr_node], sqr_dis

  
    curr_best_nodes = [curr_node] 
    curr_best_sqr_dis = np.sum((np.array(query) - np.array(curr_node.get_position())) ** 2)

    if curr_node.left is not None:
      best_left_children, best_left_sqr_dis = self.nearest_neighbor(query, curr_node.left, (level+1)%self.dim)
      if best_left_sqr_dis < curr_best_sqr_dis:
        curr_best_nodes = best_left_children
        curr_best_sqr_dis = best_left_sqr_dis
      elif best_left_sqr_dis == curr_best_sqr_dis:
        curr_best_nodes += best_left_children

    if curr_node.right is not None:

      axis_sqr_dis = (query[level] - curr_node.get_position()[level]) ** 2
      if axis_sqr_dis < curr_best_sqr_dis:
        best_right_children, best_right_sqr_dis = self.nearest_neighbor(query, curr_node.right, (level+1)%self.dim)
        if best_right_sqr_dis < curr_best_sqr_dis:
          curr_best_nodes = best_right_children
          curr_best_sqr_dis = best_right_sqr_dis
        elif best_right_sqr_dis == curr_best_sqr_dis:
          curr_best_nodes += best_right_children

    return curr_best_nodes, curr_best_sqr_dis

  def k_nearest_neighbors(self, query, curr_node, k, level):
    if curr_node.left is None and curr_node.right is None:
      sqr_dis = np.sum((np.array(query) - np.array(curr_node.get_position())) ** 2)
      return [curr_node], [sqr_dis]
    curr_best_nodes = [curr_node] 
    curr_best_sqr_dis = [np.sum((np.array(query) - np.array(curr_node.get_position())) ** 2)]
    if curr_node.left is not None:
      
      best_left_children, best_left_sqr_dis = self.k_nearest_neighbors(query, curr_node.left, k, (level+1)%self.dim)

      if len(best_left_children) < k or curr_best_sqr_dis[0] < best_left_sqr_dis[-1]:
        idx = bisect(best_left_sqr_dis, curr_best_sqr_dis[0])
        best_left_sqr_dis.insert(idx, curr_best_sqr_dis[0])
        best_left_children.insert(idx, curr_best_nodes[0])

      curr_best_nodes = best_left_children[:k]
      curr_best_sqr_dis = best_left_sqr_dis[:k]

    if curr_node.right is not None:

      axis_sqr_dis = (query[level] - curr_node.get_position()[level]) ** 2

      if len(curr_best_nodes) < k or curr_best_sqr_dis[-1] > axis_sqr_dis:
       
        best_right_children, best_right_sqr_dis = self.k_nearest_neighbors(query, curr_node.right, k, (level+1)%self.dim)
   
        tmp_dis = []
        tmp_nodes = []
        curr_idx = 0
        right_idx = 0
        while right_idx<len(best_right_sqr_dis) and curr_idx<len(curr_best_sqr_dis) and len(tmp_dis)<k:
          if best_right_sqr_dis[right_idx] < curr_best_sqr_dis[curr_idx]:
            tmp_dis.append(best_right_sqr_dis[right_idx])
            tmp_nodes.append(best_right_children[right_idx])
            right_idx += 1
          else:
            tmp_dis.append(curr_best_sqr_dis[curr_idx])
            tmp_nodes.append(curr_best_nodes[curr_idx])
            curr_idx += 1

        tmp_size = len(tmp_dis)
        if tmp_size < k:

          if curr_idx == len(curr_best_sqr_dis):
        
            tmp_dis += best_right_sqr_dis[right_idx:min(right_idx+k-tmp_size,len(best_right_sqr_dis))]
            tmp_nodes += best_right_children[right_idx:min(right_idx+k-tmp_size,len(best_right_children))]
          elif right_idx == len(best_right_sqr_dis):
            tmp_dis += curr_best_sqr_dis[curr_idx:min(curr_idx+k-tmp_size,len(curr_best_sqr_dis))]
            tmp_nodes += curr_best_nodes[curr_idx:min(curr_idx+k-tmp_size,len(curr_best_nodes))]

        curr_best_nodes = tmp_nodes
        curr_best_sqr_dis = tmp_dis

    return curr_best_nodes, curr_best_sqr_dis



def main():
  
  tree = KDTree(df.to_numpy())

  nn,_ = tree.nearest_neighbor((7.0, 6.0, 1.0), tree.root, 0)
  print ('The cloest neighbor for query point (7.0, 6.0, 1.0):')
  for node in nn:
    print(node.get_position())

  print ('\n')

  k =3
  print ('The %d nearest neighbors for query point (8.0, 3.0, 1.0):' % k)
  nn, _ = tree.k_nearest_neighbors((8.0,3.0, 1.0), tree.root, k, 0)
  for node in nn:
    print(node.get_position())


if __name__ == "__main__":
  data_prueba = np.loadtxt('./test/2dpt.txt', delimiter=",")
  df=pd.DataFrame(data_prueba)
  print(df.to_numpy())
  main()
