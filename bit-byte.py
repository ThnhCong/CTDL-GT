import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

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


def compress_file(input_file, output_bin, output_code_table, binary_view_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Xây cây và mã
    root = build_huffman_tree(text)
    codes = build_codes(root)

    # Mã hóa văn bản thành chuỗi bit
    encoded_text = "".join(codes[ch] for ch in text)

    # Thêm padding cho đủ bội 8
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text

    # Ghi file nhị phân
    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))
    with open(output_bin, "wb") as f:
        f.write(b)

    # Ghi bảng mã Huffman
    with open(output_code_table, "w", encoding="utf-8") as f:
        for ch, code in codes.items():
            if ch == "\n":
                f.write("\\n:" + code + "\n")
            elif ch == " ":
                f.write("space:" + code + "\n")
            else:
                f.write(f"{ch}:{code}\n")

    # Ghi chuỗi nhị phân ra file text để xem
    with open(binary_view_file, "w", encoding="utf-8") as f:
        f.write(encoded_text)

    print(" Đã nén thành công!")
    print(f"--> File nhị phân: {output_bin}")
    print(f"--> Bảng mã: {output_code_table}")
    print(f"--> Mã nhị phân xem được: {binary_view_file}")


# -------------------------------
# 5️⃣ Giải nén file
# -------------------------------
def decompress_file(input_bin, input_code_table, output_text):
    # Đọc bảng mã
    codes = {}
    with open(input_code_table, "r", encoding="utf-8") as f:
        for line in f:
            if ":" not in line:
                continue
            ch, code = line.strip().split(":", 1)
            if ch == "\\n":
                codes[code] = "\n"
            elif ch == "space":
                codes[code] = " "
            else:
                codes[code] = ch

    # Đọc file nhị phân
    with open(input_bin, "rb") as f:
        bit_string = ""
        byte = f.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits
            byte = f.read(1)

    # Bỏ padding
    padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-padding]

    # Giải mã
    current_code = ""
    decoded_text = ""
    for bit in bit_string:
        current_code += bit
        if current_code in codes:
            decoded_text += codes[current_code]
            current_code = ""

    with open(output_text, "w", encoding="utf-8") as f:
        f.write(decoded_text)

    print(" Giải nén thành công!")
    print(f"--> File văn bản: {output_text}")


if __name__ == "__main__":
    compress_file("input.txt", "compressed.bin", "code_table.txt", "binary_view.txt")
    decompress_file("compressed.bin", "code_table.txt", "output.txt")
