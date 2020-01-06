def text_to_binary_blocks(fileName):
    bytes_list = b""

    with open(fileName, "rb") as f:
        while True:
            c = f.read(1)
            if not c:
                break
            
            else:
                bytes_list += c
    binary_msg = ""
    for b in bytes_list:
        print(bin(b), end=" ")
        size = len(bin(b)[2:])
        while size < 8:
            binary_msg += "0"
            size += 1
        binary_msg += bin(b)[2:]# + " "

    rest = len(binary_msg) % 64
    while rest < 64:
        binary_msg += "0"
        rest += 1
    blocks = dict()
    for i in range(int(len(binary_msg)/64)):
        blocks[i] = binary_msg[64*i:64*i+64]
    return(blocks)

blocks = text_to_binary_blocks("Messages/Chiffrement_DES_de_1.txt")

for i in range(len(blocks)):
    print(blocks[i])