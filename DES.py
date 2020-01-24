from ConvAlphaBin import conv_bin, nib_vnoc
from MY_Extract_ConstantesDES import recupConstantesDES
from utils import *

fileID = "6" #Could be "1", "2", "3", "4", "5", "6"
i_want_to_decrypt = True

def C_DES(M, X, Kx):
    Mx = binary_string_to_blocks(M)
    new_M = ""

    for k in range(len(Mx)):
        PM1 = apply_matrix(Mx[k], X["PI"])
        G = dict_to_string(PM1)[:32]
        D = dict_to_string(PM1)[32:]

        for j in range(16):
            E = apply_matrix(D, X["E"])
            xorE = apply_xor(E, Kx[j])
            blocks = list()
            for i in range(int(len(xorE)/6)):
                blocks.append(xorE[6*i:6*i+6])

            for i in range(8):
                line = int('0b' + blocks[i][0] + blocks[i][5], 2)
                column = int('0b' + blocks[i][1:5], 2)

                S = X["S"+str(i+1)]
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
            res = apply_matrix(blocks_string, X["PERM"])
            save_D = D
            D = apply_xor(res, G)
            G = save_D
        new_M += apply_matrix(G + D, X["PI_I"])
    return(new_M)

def D_DES(M, X, Kx):
    Mx = binary_string_to_blocks(M)
    new_M = ""

    for k in range(len(Mx)):
        PM1 = apply_matrix(Mx[k], X["PI"])
        G = dict_to_string(PM1)[32:]
        D = dict_to_string(PM1)[:32]

        for j in range(15, -1, -1):
            E = apply_matrix(D, X["E"])
            xorE = apply_xor(E, Kx[j])
            blocks = list()
            for i in range(int(len(xorE)/6)):
                blocks.append(xorE[6*i:6*i+6])

            for i in range(8):
                line = int('0b' + blocks[i][0] + blocks[i][5], 2)
                column = int('0b' + blocks[i][1:5], 2)

                S = X["S"+str(i+1)]
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
            res = apply_matrix(blocks_string, X["PERM"])
            save_D = D
            D = apply_xor(res, G)
            G = save_D
        new_M += apply_matrix(D + G, X["PI_I"])

    return(new_M)


clefs=["PI","PI_I","E","PERM","CP_1","CP_2","S1","S2","S3","S4","S5","S6","S7","S8"]
X = recupConstantesDES(clefs)
for i in range(8):
    X["S"+str(i+1)] = change_dict_to_matrix(X["S"+str(i+1)])

Kx = generate_Kx(read_file("Messages/Clef_de_" + fileID + ".txt"), X)
base = read_file("Messages/Chiffrement_DES_de_" + fileID + ".txt")

if(i_want_to_decrypt):
    res = D_DES(conv_bin(base), X, Kx)
else:
    res = C_DES(conv_bin(base), X, Kx)

print(nib_vnoc(res))

