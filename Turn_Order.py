from BattleTroop import BattleTroop

class PriorityQueue():
  def __init__(self):
    self.queue = []

  def is_empty(self):
    return len(self.queue) == 0

  def less_than_two(self):
    return len(self.queue) < 2
    
  # Rules for queueing an troop in the queue:
  # - If faster than everything add to front of queue
  # - If slower than or same speed as last thing add to back of queue
  # - If same speed as another then add new troop after old troop
  def enqueue(self, troop):
    if type(troop) is BattleTroop:
      if self.less_than_two():
        if self.is_empty() or self.queue[0].action <= troop.action:
          self.queue.append(troop)
        else:
          self.queue.insert(0,troop)
      elif troop.action >= self.queue[-1].action:
        self.queue.append(troop)
      elif troop.action < self.queue[0].action:
        self.queue.insert(0,troop)
      else:
        for i,x in enumerate(self.queue):
          if troop.action >= x.action and troop.action < self.queue[i+1].action:
            self.queue.insert(i+1,troop)
            break
    else:
      raise TypeError("Invalid troop type.")

  def dequeue(self, pos=0):
    if pos == -1: return
    try:
      return self.queue.pop(pos)
    except IndexError:
      exit()

  def get_pos(self, troop):
    for i,x in enumerate(self.queue):
      if troop is x:
        return i
    return -1

  def to_zero(self):
    dequeue = self.queue[0].action
    for i in self.queue:
      i.action -= dequeue
    return dequeue

if __name__ == '__main__':
    pass
