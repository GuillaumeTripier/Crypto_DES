from ConvAlphaBin import conv_bin, nib_vnoc
#from Extract_ConstantesDES import recupConstantesDES

def get_dict_from_string(source):
    result = dict()
    string_splited = source.split(" ")
    for i in range(len(string_splited)):
        result[i] = string_splited[i]
    return(result)

def get_matrix_from_string(source):
    result = list()
    string_splited = source.split(" ")
    for i in range(int(len(string_splited)/16)):
        result.append(string_splited[16*i:16*i+16])
    return(result)


def get_binary_string_from_file(fileName):
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
        #print(bin(b), end=" ")
        size = len(bin(b)[2:])
        while size < 8:
            binary_msg += "0"
            size += 1
        binary_msg += bin(b)[2:]# + " "

    return(binary_msg)

def binary_string_to_blocks(source):
    rest = len(source) % 64
    while rest < 64:
        source += "0"
        rest += 1
    blocks = list()
    for i in range(int(len(source)/64)):
        blocks.append(source[64*i:64*i+64])
    return(blocks)

def extract_key_full_from_file(fileName):
    data = ""
    with open(fileName, "r") as f:
        data = f.read()
    ##########
    data = "0101111001011011010100100111111101010001000110101011110010010001"
    #########
    return(data)

def check_dif(str1, str2):
    assert(str1 == str2)

def dict_to_string(source):
    result = ""
    for i in range(len(source)):
        result += source[i]
    return(result)

def apply_matrix(source, matrixx):
    result = ""
    for i in range(len(matrixx)):
        result += source[int(matrixx[i])-1]
    return(result)

def remove_matrix(source, matrixx):
    my_dict = dict()
    for i in range(len(matrixx)):
        my_dict[int(matrixx[i])-1] = source[i]
    result = dict_to_string(my_dict)
    return(result)

def apply_xor(source, K):
    result = ""
    for i in range(len(source)):
        if source[i] == K[i]:
            result += "0"
        else:
            result += "1"
    return(result)

def C_DES(M):
    Mx = binary_string_to_blocks(M)
    new_M = ""

    for k in range(1):#len(Mx)):
        PM1 = apply_matrix(Mx[k], get_dict_from_string(string_PI))
        G = dict_to_string(PM1)[:32]
        D = dict_to_string(PM1)[32:]

        for j in range(16):
            E = apply_matrix(D, get_dict_from_string(string_E))
            xorE = apply_xor(E, Kx[j])
            blocks = list()
            for i in range(int(len(xorE)/6)):
                blocks.append(xorE[6*i:6*i+6])

            for i in range(8):
                line = int('0b' + blocks[i][0] + blocks[i][5], 2)
                column = int('0b' + blocks[i][1:5], 2)

                S = get_matrix_from_string(Sx[i])
                short_binary_string = bin(int(S[line][column]))[2:]
                new_block = ""
                rest = 4 - len(short_binary_string)
                while rest != 0:
                    new_block += "0"
                    rest -= 1
                new_block += short_binary_string
                blocks[i] = new_block
            blocks_string = ""
            for i in blocks:
                blocks_string += i
            res = apply_matrix(blocks_string, get_dict_from_string(string_P))
            save_D = D
            D = apply_xor(res, G)
            G = save_D
        new_M += apply_matrix(G + D, get_dict_from_string(string_PI_inverse))
    return(new_M)

def D_DES(M):
    Mx = binary_string_to_blocks(M)
    #print(Mx)
    new_M = ""

    for k in range(len(Mx)):
        PM1 = apply_matrix(Mx[k], get_dict_from_string(string_PI))
        G = dict_to_string(PM1)[:32]
        D = dict_to_string(PM1)[32:]

        for j in range(16):
            E = apply_matrix(D, get_dict_from_string(string_E))
            xorE = apply_xor(E, Kx[len(Kx)-1-j])
            blocks = list()
            for i in range(int(len(xorE)/6)):
                blocks.append(xorE[6*i:6*i+6])

            for i in range(8):
                line = int('0b' + blocks[i][0] + blocks[i][5], 2)
                column = int('0b' + blocks[i][1:5], 2)

                S = get_matrix_from_string(Sx[i])
                short_binary_string = bin(int(S[line][column]))[2:]
                new_block = ""
                rest = 4 - len(short_binary_string)
                while rest != 0:
                    new_block += "0"
                    rest -= 1
                new_block += short_binary_string
                blocks[i] = new_block
            blocks_string = ""
            for i in blocks:
                blocks_string += i
            res = apply_matrix(blocks_string, get_dict_from_string(string_P))
            save_D = D
            D = apply_xor(res, G)
            G = save_D
        new_M += apply_matrix(G + D, get_dict_from_string(string_PI_inverse))

    return(new_M)

string_PI = "58 50 42 34 26 18 10 2 60 52 44 36 28 20 12 4 62 54 46 38 30 22 14 6 64 56 48 40 32 24 16 8 57 49 41 33 25 17 9 1 59 51 43 35 27 19 11 3 61 53 45 37 29 21 13 5 63 55 47 39 31 23 15 7"
string_PI_inverse = "40 8 48 16 56 24 64 32 39 7 47 15 55 23 63 31 38 6 46 14 54 22 62 30 37 5 45 13 53 21 61 29 36 4 44 12 52 20 60 28 35 3 43 11 51 19 59 27 34 2 42 10 50 18 58 26 33 1 41 9 49 17 57 25"
string_P = "16 7 20 21 29 12 28 17 1 15 23 26 5 18 31 10 2 8 24 14 32 27 3 9 19 13 30 6 22 11 4 25"
string_CP1 = "57 49 41 33 25 17 9 1 58 50 42 34 26 18 10 2 59 51 43 35 27 19 11 3 60 52 44 36 63 55 47 39 31 23 15 7 62 54 46 38 30 22 14 6 61 53 45 37 29 21 13 5 28 20 12 4"
string_CP2 = "14 17 11 24 1 5 3 28 15 6 21 10 23 19 12 4 26 8 16 7 27 20 13 2 41 52 31 37 47 55 30 40 51 45 33 48 44 49 39 56 34 53 46 42 50 36 29 32"
string_E = "32 1 2 3 4 5 4 5 6 7 8 9 8 9 10 11 12 13 12 13 14 15 16 17 16 17 18 19 20 21 20 21 22 23 24 25 24 25 26 27 28 29 28 29 30 31 32 1"
string_S1 = "14 4 13 1 2 15 11 8 3 10 6 12 5 9 0 7 0 15 7 4 14 2 13 1 10 6 12 11 9 5 3 8 4 1 14 8 13 6 2 11 15 12 9 7 3 10 5 0 15 12 8 2 4 9 1 7 5 11 3 14 10 0 6 13"
string_S2 = "15 1 8 14 6 11 3 4 9 7 2 13 12 0 5 10 3 13 4 7 15 2 8 14 12 0 1 10 6 9 11 5 0 14 7 11 10 4 13 1 5 8 12 6 9 3 2 15 13 8 10 1 3 15 4 2 11 6 7 12 0 5 14 9"
string_S3 = "10 0 9 14 6 3 15 5 1 13 12 7 11 4 2 8 13 7 0 9 3 4 6 10 2 8 5 14 12 11 15 1 13 6 4 9 8 15 3 0 11 1 2 12 5 10 14 7 1 10 13 0 6 9 8 7 4 15 14 3 11 5 2 12"
string_S4 = "7 13 14 3 0 6 9 10 1 2 8 5 11 12 4 15 13 8 11 5 6 15 0 3 4 7 2 12 1 10 14 9 10 6 9 0 12 11 7 13 15 1 3 14 5 2 8 4 3 15 0 6 10 1 13 8 9 4 5 11 12 7 2 14"
string_S5 = "2 12 4 1 7 10 11 6 8 5 3 15 13 0 14 9 14 11 2 12 4 7 13 1 5 0 15 10 3 9 8 6 4 2 1 11 10 13 7 8 15 9 12 5 6 3 0 14 11 8 12 7 1 14 2 13 6 15 0 9 10 4 5 3"
string_S6 = "12 1 10 15 9 2 6 8 0 13 3 4 14 7 5 11 10 15 4 2 7 12 9 5 6 1 13 14 0 11 3 8 9 14 15 5 2 8 12 3 7 0 4 10 1 13 11 6 4 3 2 12 9 5 15 10 11 14 1 7 6 0 8 13"
string_S7 = "4 11 2 14 15 0 8 13 3 12 9 7 5 10 6 1 13 0 11 7 4 9 1 10 14 3 5 12 2 15 8 6 1 4 11 13 12 3 7 14 10 15 6 8 0 5 9 2 6 11 13 8 1 4 10 7 9 5 0 15 14 2 3 12"
string_S8 = "13 2 8 4 6 15 11 1 10 9 3 14 5 0 12 7 1 15 13 8 10 3 7 4 12 5 6 11 0 14 9 2 7 11 4 1 9 12 14 2 0 6 10 13 15 3 5 8 2 1 14 7 4 10 8 13 15 12 9 0 3 5 6 11"
Sx = list()
Sx.append(string_S1)
Sx.append(string_S2)
Sx.append(string_S3)
Sx.append(string_S4)
Sx.append(string_S5)
Sx.append(string_S6)
Sx.append(string_S7)
Sx.append(string_S8)

K = extract_key_full_from_file("Messages/Clef_de_1.txt")
GD = apply_matrix(K, get_dict_from_string(string_CP1))
check_dif(dict_to_string(GD),"11000000000111110100100011110010111101001001011010111111")
CP2 = get_dict_from_string(string_CP2)
G = dict_to_string(GD)[:28]
D = dict_to_string(GD)[28:]

Kx = list()
for i in range(16):
    G = G[1:] + G[0]
    D = D[1:] + D[0]
    GD = G + D
    Kx.append(apply_matrix(GD, CP2))

#M = "1101110010111011110001001101010111100110111101111100001000110010100111010010101101101011111000110011101011011111"
#print(C_DES(M))
#check_dif(C_DES(M), "10001000001101101010000100010011110010110110000010010100100100000010011101110000010110100010000000001101000100011100011011000100")
#check_dif(nib_vnoc(C_DES(M)), "iDahEètglJAncFogDRHGxA")
#check_dif(conv_bin("iDahEètglJAncFogDRHGxA"), C_DES(M)+"0000")


"""res1 = dict_to_string(binary_string_to_blocks("1000100000110110101000010001001111001011011000001001010010010000"))#"Messages/Chiffrement_DES_de_1.txt")))
data = ""
with open("Messages/Chiffrement_DES_de_1.txt", "r") as f:
    data = f.read()
##########
#data = "0101111001011011010100100111111101010001000110101011110010010001"
#########
res2 = conv_bin("iDahEètglJA")
print("\n", res1, res2)
print(nib_vnoc("1000100000110110101000010001001111001011011000001001010010010000"))
#check_dif(res1, res2)"""

base = "!LvE.eb!wjI"
check_dif(nib_vnoc(conv_bin(base)), base)
check_dif(conv_bin(base), "1101110010111011110001001101010111100110111101111100001000110010" +"00")
res = C_DES(conv_bin(base))
#print(res)
check_dif(res, "1000100000110110101000010001001111001011011000001001010010010000")
check_dif(nib_vnoc(res), "iDahEètglJA")

print(D_DES(res))
print("1101110010111011110001001101010111100110111101111100001000110010")

PM_I = "0111110110101011001111010010101001111111101100100000001111110010"
expected = "1101110010111011110001001101010111100110111101111100001000110010"

res2 = remove_matrix(PM_I, get_dict_from_string(string_PI))
check_dif(res2, expected)







PM_I = "1000100000110110101000010001001111001011011000001001010010010000"
M = remove_matrix(PM_I, get_dict_from_string(string_PI_inverse))
check_dif(M, "0011000011001010010000100001110011010101001001100001000100011010")
G = dict_to_string(M)[:32]
D = dict_to_string(M)[32:]
check_dif(G, "00110000110010100100001000011100")
check_dif(D, "11010101001001100001000100011010")

goal_G = "01100111100101000101100001000001"
goal_D = "00110000110010100100001000011100"

res = apply_xor(G, D)
save_D = D
D = G
check_dif(D, goal_D)
#print(res)
#check_dif(G, goal_G)





#res = remove_matrix(D, get_dict_from_string(string_P))
#G = res
#print(res)
pre_G=     "01111111101100100000001111110010"
pre_D=     "11011110111011001101000011001100"
objectif_G="01111101101010110011110100101010"
objectif_D="01111111101100100000001111110010"

"""res = apply_xor(pre_G, pre_D)
pre_D = pre_G
#res = remove_matrix(D, get_dict_from_string(string_P))
pre_G = res
print(res)
print("10100011010001111110110111100110")
check_dif(pre_D, objectif_D)
check_dif(pre_G, objectif_G)"""
