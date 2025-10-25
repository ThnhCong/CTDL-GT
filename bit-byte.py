#cong va nhan
import heapq
import os
from collections import Counter

# -------------------------------
# 1. Xây cây Huffman
# -------------------------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Để so sánh trong heapq
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(ch, freq) for ch, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left, merged.right = n1, n2
        heapq.heappush(heap, merged)

    return heap[0]  # root


# -------------------------------
# 2. Tạo bảng mã Huffman
# -------------------------------
def build_codes(node, current_code="", codes={}):
    if node is None:
        return

    if node.char is not None:
        codes[node.char] = current_code
        return

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes


# -------------------------------
# 3. Nén văn bản thành bit
# -------------------------------
def huffman_encode(text, codes):
    encoded_text = "".join(codes[ch] for ch in text)
    # Đệm bit cho đủ byte
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text

    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))

    return bytes(b)


# -------------------------------
# 4. Giải nén Huffman
# -------------------------------
def huffman_decode(encoded_bytes, codes):
    bit_string = ""
    for byte in encoded_bytes:
        bit_string += "{0:08b}".format(byte)

    # Bỏ padding
    extra_padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-extra_padding]

    reverse_codes = {v: k for k, v in codes.items()}

    current_bits = ""
    decoded_text = ""
    for bit in bit_string:
        current_bits += bit
        if current_bits in reverse_codes:
            decoded_text += reverse_codes[current_bits]
            current_bits = ""

    return decoded_text


# -------------------------------
# 5. Chạy chương trình chính
# -------------------------------
def compress_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded_bytes = huffman_encode(text, codes)

    with open(output_path, "wb") as f:
        f.write(encoded_bytes)

    print("✅ Đã nén xong.")
    print("Dung lượng gốc:", os.path.getsize(input_path), "bytes")
    print("Dung lượng sau nén:", os.path.getsize(output_path), "bytes")

    return codes


def decompress_file(input_path, output_path, codes):
    with open(input_path, "rb") as f:
        encoded_bytes = f.read()

    decoded_text = huffman_decode(encoded_bytes, codes)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decoded_text)

    print("✅ Giải nén xong.")


# -------------------------------
# 6. Ví dụ sử dụng
# -------------------------------
if __name__ == "__main__":
    codes = compress_file("input.txt", "compressed.bin")
    decompress_file("compressed.bin", "output.txt", codes)
