import heapq
import json
from collections import Counter

# -------------------------------
# 1️⃣ Định nghĩa node cây Huffman
# -------------------------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Cho phép so sánh node trong heapq
    def __lt__(self, other):
        return self.freq < other.freq


# -------------------------------
# 2️⃣ Xây cây Huffman từ dữ liệu
# -------------------------------
def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]


# -------------------------------
# 3️⃣ Tạo bảng mã (ký tự → chuỗi bit)
# -------------------------------
def build_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes

    if node.char is not None:
        codes[node.char] = current_code
        return codes

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)
    return codes


# -------------------------------
# 4️⃣ Hàm nén file
# -------------------------------
def compress_file(input_file, output_bin, output_json):
    # Đọc nội dung file
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Xây cây Huffman và bảng mã
    root = build_huffman_tree(text)
    codes = build_codes(root)

    # Mã hóa toàn bộ nội dung
    encoded_text = "".join(codes[ch] for ch in text)

    # Thêm phần đệm để đủ bội 8
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding

    # Ghi số lượng padding vào 8 bit đầu tiên
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text

    # Chuyển sang byte
    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        b.append(int(byte, 2))

    # Ghi file nhị phân
    with open(output_bin, "wb") as out:
        out.write(bytes(b))

    # Ghi bảng mã (cấu trúc cây Huffman)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=4)

    print("✅ Đã nén xong!")
    print(f"--> File nén: {output_bin}")
    print(f"--> Cây Huffman: {output_json}")


# -------------------------------
# 5️⃣ Hàm giải nén file
# -------------------------------
def decompress_file(input_bin, input_json, output_file):
    # Đọc bảng mã Huffman
    with open(input_json, "r", encoding="utf-8") as f:
        codes = json.load(f)

    # Đảo bảng mã (bit → ký tự)
    reversed_codes = {v: k for k, v in codes.items()}

    # Đọc dữ liệu nén
    with open(input_bin, "rb") as f:
        bit_string = ""
        byte = f.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits
            byte = f.read(1)

    # Gỡ padding
    padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-padding]

    # Giải mã
    current_code = ""
    decoded_text = ""
    for bit in bit_string:
        current_code += bit
        if current_code in reversed_codes:
            decoded_text += reversed_codes[current_code]
            current_code = ""

    # Ghi ra file văn bản
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(decoded_text)

    print("✅ Giải nén thành công!")
    print(f"--> File kết quả: {output_file}")


# -------------------------------
# 6️⃣ Ví dụ chạy thử
# -------------------------------
if __name__ == "__main__":
    compress_file("input.txt", "compressed.bin", "huffman_tree.json")
    decompress_file("compressed.bin", "huffman_tree.json", "output.txt")
