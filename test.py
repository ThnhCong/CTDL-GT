import heapq
from collections import Counter

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

print(" Nội dung file:")
print(text)

freq = Counter(text)
print("\n Tần suất xuất hiện của từng ký tự:")
for char, count in freq.items():
    if char == "\n":
        print("'\\n':", count)
    elif char == " ":
        print("'space':", count)
    else:
        print(f"'{char}':", count)

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

heap = [Node(char, f) for char, f in freq.items()]
heapq.heapify(heap)

while len(heap) > 1:
    n1 = heapq.heappop(heap)
    n2 = heapq.heappop(heap)
    merged = Node(None, n1.freq + n2.freq)
    merged.left = n1
    merged.right = n2
    heapq.heappush(heap, merged)

root = heap[0]

codes = {}
def generate_codes(node, current_code=""):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
        return
    generate_codes(node.left, current_code + "0")
    generate_codes(node.right, current_code + "1")

generate_codes(root)

print("\n Bảng mã Huffman:")
for char, code in codes.items():
    if char == "\n":
        print("'\\n':", code)
    elif char == " ":
        print("'space':", code)
    else:
        print(f"'{char}': {code}")

encoded_text = "".join(codes[ch] for ch in text)

padding = 8 - len(encoded_text) % 8
if padding == 8:
    padding = 0
else:
    encoded_text += "0" * padding

print("\n Chuỗi bit mã hóa:")
print(encoded_text)

print(f"\n Độ dài mã bit: {len(encoded_text)} bits (bao gồm {padding} bit đệm nếu có)")