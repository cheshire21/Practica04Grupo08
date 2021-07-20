import pandas as pd
import numpy as np
from node import Node
from bisect import bisect
import math

class KDTree(object):
  def __init__(self, X_train, Y_train):
    # self.pc_path = file_path
    self.dim = X_train.shape[1]


    self.points = X_train
    self.labels = Y_train

    self.root = self.build_kdtree_mejorado(self.points,self.labels, 0)

  def build_kdtree_mejorado(self,points, labels, depth=0):
    n=len(points)
    axis=depth % self.dim
    if(n<=0):
      return None
    if(n==1):
      return Node(points[0],labels[0],axis)
    median=math.floor(len(points)/2)
    
    #points.sort(key=(lambda a,b: a[axis]-b[axis]))
    # print(points.shape)
    labels = labels[points[:, axis].argsort(kind='mergesort')]
    points = points[points[:, axis].argsort(kind='mergesort')]
    
    
    points_left=points[0:median]
    points_right=points[median+1:]

    labels_left=labels[0:median]
    labels_right=labels[median+1:]

    node=Node(points[median],labels[median],axis)
    node.left=self.build_kdtree_mejorado(points_left,labels_left,depth+1)
    node.right=self.build_kdtree_mejorado(points_right,labels_right,depth+1)

    return node

  def KNN(self, query, curr_node, k, level):
    if curr_node.left is None and curr_node.right is None:
      sqr_dis = np.sum((np.array(query) - np.array(curr_node.get_position())) ** 2)
      return [curr_node], [sqr_dis]
    curr_best_nodes = [curr_node] 
    curr_best_sqr_dis = [np.sum((np.array(query) - np.array(curr_node.get_position())) ** 2)]
    if curr_node.left is not None:
      
      best_left_children, best_left_sqr_dis = self.KNN(query, curr_node.left, k, (level+1)%self.dim)

      if len(best_left_children) < k or curr_best_sqr_dis[0] < best_left_sqr_dis[-1]:
        idx = bisect(best_left_sqr_dis, curr_best_sqr_dis[0])
        best_left_sqr_dis.insert(idx, curr_best_sqr_dis[0])
        best_left_children.insert(idx, curr_best_nodes[0])

      curr_best_nodes = best_left_children[:k]
      curr_best_sqr_dis = best_left_sqr_dis[:k]

    if curr_node.right is not None:

      axis_sqr_dis = (query[level] - curr_node.get_position()[level]) ** 2

      if len(curr_best_nodes) < k or curr_best_sqr_dis[-1] > axis_sqr_dis:
       
        best_right_children, best_right_sqr_dis = self.KNN(query, curr_node.right, k, (level+1)%self.dim)
   
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