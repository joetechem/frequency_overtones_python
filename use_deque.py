from collections import deque
d = deque(range(10))
print(d)

d.append(-1)
print(d)

d.popleft()

print(d)
