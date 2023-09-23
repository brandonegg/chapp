class PriorityQueue:

  def __init__(self):
    self.queue = [] # elements (priority, item)

  def push(self, item, priority):
    insert_at = len(self.queue)

    for i, element in enumerate(self.queue):
      element_priority = element[0]
      if element_priority > priority:
        insert_at = i
        break

    new_queue = self.queue[:insert_at] + [(priority, item)]
    if len(self.queue) > 0:
      new_queue += self.queue[insert_at:]

    self.queue = new_queue

  def pop(self):
    return self.queue.pop(0)[1]
  
  def len(self):
    return len(self.queue)


# Tests
if __name__ == "__main__":
  queue = PriorityQueue()
  queue.push("second", 2) # [("second", 2)]
  print(queue.queue)
  queue.push("first", 1) # [("first", 1), ("second", 2)]
  print(queue.queue)
  queue.push("fourth", 4) # [("first", 1), ("second", 2), ("fourth", 4)]
  print(queue.queue)
  queue.push("third", 3) # [("first", 1), ("second", 2), ("third", 3), ("fourth", 4)]
  print(queue.queue)

  print(queue.pop())
  