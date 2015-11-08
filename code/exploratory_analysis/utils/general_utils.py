from itertools import product

def vol_index_iter(shape):
  return product(range(shape[0]), range(shape[1]), range(shape[2]))