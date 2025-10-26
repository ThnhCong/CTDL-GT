from collections import Counter
import heapq

from pkg_resources import non_empty_lines

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Nội dung file:")
print(text)

freq = Counter(text)

print("\n frequence of character:")
for char, count in freq.item():
    print(f"'{char}': {count}")

class Node:
    def __init__(self, char, freg):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

heap = [Node(char, f) for char, f in freq.item()]
heapq.heapify(heap)

while len(heap) > 1:
    n1 = heapq.heappop(heap)
    n2 = heapq.heappop(heap)
    merged = Node(None, n1.freq + n2.freq)
    merged.left = n1
    merged.right = n2
    heapq.heappush(heap, merged)

root = heap[0]
