def get_matrix_from_string(source):
    result = list()
    string_splited = source.split(" ")
    for i in range(int(len(string_splited)/16)):
        result.append(string_splited[16*i:16*i+16])
    return(result)

def binary_string_to_blocks(source):
    rest = len(source) % 64
    while rest < 64 and rest != 0:
        source += "0"
        rest += 1
    blocks = list()
    for i in range(int(len(source)/64)):
        blocks.append(source[64*i:64*i+64])
    
    return(blocks)

def read_file(fileName):
    data = ""
    with open(fileName, "r") as f:
        data = f.read()
    return(data)

def dict_to_string(source):
    result = ""
    for i in range(len(source)):
        result += source[i]
    return(result)

def change_dict_to_matrix(source):
    result = ""
    for i in range(len(source)):
        result += source[i] + ' '
    return(get_matrix_from_string(result[:-1]))

def apply_matrix(source, matrixx):
    result = ""
    for i in range(len(matrixx)):
        result += source[int(matrixx[i])-1]
    return(result)

def apply_xor(source, K):
    result = ""
    for i in range(len(source)):
        if source[i] == K[i]:
            result += "0"
        else:
            result += "1"
    return(result)

def generate_Kx(K, X):
    GD = apply_matrix(K, X["CP_1"])
    G = dict_to_string(GD)[:28]
    D = dict_to_string(GD)[28:]
    
    Kx = list()
    for i in range(16):
        G = G[1:] + G[0]
        D = D[1:] + D[0]
        GD = G + D
        Kx.append(apply_matrix(GD, X["CP_2"]))
    return(Kx)
