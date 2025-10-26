from collections import Counter
import heapq

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

print(" Nội dung file:")
print(text)

freq = Counter(text)
print("\n📊 Tần suất xuất hiện ký tự:")
for char, count in freq.items():
    if char == "\n":
        print("'\\n':", count)
    elif char == " ":
        print("'space':", count)
    else:
        print(f"'{char}': {count}")

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
print("\n Chuỗi bit mã hóa:")
print(encoded_text)

padding = 8 - len(encoded_text) % 8
encoded_text += "0" * padding
padding_info = "{0:08b}".format(padding)
binary_data = padding_info + encoded_text

b = bytearray()
for i in range(0, len(binary_data), 8):
    byte = binary_data[i:i+8]
    b.append(int(byte, 2))

with open("output.bin", "wb") as f:
    f.write(bytes(b))

print(f"\n Đã lưu file nhị phân: output.bin ({len(b)} bytes)")

def decode_text(encoded_text, root):
    decoded = ""
    node = root
    for bit in encoded_text:
        node = node.left if bit == "0" else node.right
        if node.char is not None:
            decoded += node.char
            node = root
    return decoded

decoded_text = decode_text(encoded_text[:-padding], root)

print("\n Giải mã lại văn bản:")
print(decoded_text)
