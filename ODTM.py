import numpy as np
import Basic as Bsc
import KS_Operators as KS_Op
import Encryption as Enc
from RF_Operators import Pi, Tau

"""
Instruction:
- ODTM.py - prepares ciphertext collections from plaintexts produced by ADTM, writes/reads them to disk,
  and provides a simple verification helper.
"""

###################################################################################################
####                       Writing the prepared blocks into a text file                        ####
###################################################################################################
def WriteDoc(ctxList: list, Address: str) -> None:
    try:
        if type(ctxList) != list:
            raise TypeError("The first input must be a list of ciphertexts.")
        else:
            flag = True
            Address = Address + "\\Ciphertexts.txt"
            Len = len(ctxList)
            with open(Address, "w") as f:
                for i in range(0, Len):
                    f.write("0x")
                    for j in range(0, 4):
                        B1 = Bsc.Int2Crumb(ctxList[i][j][1])
                        B2 = Bsc.Int2Crumb(ctxList[i][j][2])
                        num1 = 2 * ctxList[i][j][0] + B1[0]
                        f.write(Bsc.Int2Hex(num1))
                        num2 = 8 * B1[1] + 4 * B1[2] + 2 * B2[0] + B2[1]
                        f.write(Bsc.Int2Hex(num2))
                        num3 = B2[2] * 8 + ctxList[i][j][3]
                        f.write(Bsc.Int2Hex(num3))
                    f.write("\n")
                    y = round((i + 1) / Len * 100, 2)
                    if abs(y - round(y)) < 0.05 and flag == True:
                        print(f"ODTM: {round(y)}% of the writing has been completed.")
                        flag = False
                    elif abs(y - round(y)) >= 0.05:
                        flag = True
                    else:
                        continue
            f.close()

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                         Reading the plaintexts preapared by ADTM                          ####
###################################################################################################
def ReadDoc(Address: str) -> list:
    try:
        if type(Address) != str:
            raise TypeError("Input must be the address of the target file.")
        else:
            ptxList = []
            Address = Address + "\\Plaintexts.txt"
            with open(Address, "r") as f:
                Data = f.read()
                f.close()
            Len = len(Data)
            ctr = 0
            ctr2 = 0
            flag = True
            while(ctr < Len):
                if Data[ctr] == "0" and Data[ctr + 1] == "x":
                    ctr += 2
                elif Data[ctr - 2] == "0" and Data[ctr - 1] == "x":
                    ctr3 = 0
                    X = np.array([
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]
                        ], dtype = np.uint8)
                    for i in range(0, 4):
                        num1 = Bsc.Hex2Int(Data[ctr + ctr3])
                        num2 = Bsc.Hex2Int(Data[ctr + ctr3 + 1])
                        num3 = Bsc.Hex2Int(Data[ctr + ctr3 + 2])
                        outNum2 = num1 % 2
                        outNum1 = (num1 - outNum2) // 2
                        outNum3 = num2 % 4
                        outNum2 = 4 * outNum2 + (num2 - outNum3) // 4
                        outNum4 = num3 % 8
                        outNum3 = 2 * outNum3 + (num3 - outNum4) // 8
                        X[i, 0] = outNum1
                        X[i, 1] = outNum2
                        X[i, 2] = outNum3
                        X[i, 3] = outNum4
                        ctr3 += 3
                    ctr += 12
                    ptxList.append(X.copy())
                elif Data[ctr] == "\n":
                    ctr += 1
                    ctr2 += 1
                else:
                    ctr += 1
                y = round(100 * ctr / Len, 2)
                if abs(y - round(y)) < 0.05 and flag == True:
                    print(f"ODTM: {round(y)}% of the reading has been completed.")
                    flag = False
                elif abs(y - round(y)) >= 0.05:
                    flag = True
                else:
                    continue
            return ptxList

    except TypeError as e:
        print("Error: Invalid input.", e)

###################################################################################################
####                            Preparing and wrinting output data                             ####
###################################################################################################
def ODTM_Generate(Address: str) -> list:
    ptxList = ReadDoc(Address)
    N = len(ptxList)
    ctxList = []
    MK = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ], dtype = np.uint8)
    Address1 = Address + "\\MasterKey.txt"
    with open(Address1, "r") as f:
        Data = f.read()
        f.close()
    Len = len(Data)
    if Len != 14 or (Len == 15 and Data[14] != "\n"):
        raise ValueError("Master key has not been eneterd properly in the MasterKey.txt file. Please renter it properly.")
    else:
        for i in range(0, 4):
            temp = []
            for j in range(0, 3):
                y = Data[2 + i * 3 + j]
                if ord(y) > 57:
                    t = np.uint8(ord(y) - 87)
                else:
                    t = np.uint8(ord(y) - 48)
                temp.append(t)
            outNum2 = temp[0] % 2
            outNum1 = (temp[0] - outNum2) // 2
            outNum3 = temp[1] % 4
            outNum2 = 4 * outNum2 + (temp[1] - outNum3) // 4
            outNum4 = temp[2] % 8
            outNum3 = 2 * outNum3 + (temp[2] - outNum4) // 8
            MK[i][0] = outNum1
            MK[i][1] = outNum2
            MK[i][2] = outNum3
            MK[i][3] = outNum4
        flag = True
        for i in range(0, N):
            X = Enc.Enc(ptxList[i], MK, 6)
            ctxList.append(X.copy())
            y = round(100 * i / N, 2)
            if abs(y - round(y, 1)) < 0.005 and flag == True:
                print(f"ODTM: {round(y, 1)}% of the generating data has been completed.")
                flag = False
            elif abs(y - round(y, 1)) >= 0.005:
                flag = True
            else:
                continue
        WriteDoc(ctxList, Address)
        return ctxList

###################################################################################################
####   Extracting the RK* of the 6th round of nanocrypton (side info for fast key recovery)    ####
###################################################################################################
def RKst6Ext(Address: str) -> np.uint8:
    rkSt7 = np.array([0, 0, 0, 0], dtype = np.uint8)
    MK = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ], dtype = np.uint8)
    Address1 = Address + "\\MasterKey.txt"
    with open(Address1, "r") as f:
        Data = f.read()
        f.close()
    Len = len(Data)
    if Len != 14 or (Len == 15 and Data[14] != "\n"):
        raise ValueError("Master key has not been eneterd properly in the MasterKey.txt file. Please renter it properly.")
    else:
        for i in range(0, 4):
            temp = []
            for j in range(0, 3):
                y = Data[2 + i * 3 + j]
                if ord(y) > 57:
                    t = np.uint8(ord(y) - 87)
                else:
                    t = np.uint8(ord(y) - 48)
                temp.append(t)
            outNum2 = temp[0] % 2
            outNum1 = (temp[0] - outNum2) // 2
            outNum3 = temp[1] % 4
            outNum2 = 4 * outNum2 + (temp[1] - outNum3) // 4
            outNum4 = temp[2] % 8
            outNum3 = 2 * outNum3 + (temp[2] - outNum4) // 8
            MK[i][0] = outNum1
            MK[i][1] = outNum2
            MK[i][2] = outNum3
            MK[i][3] = outNum4
        KS = MK.copy()
        for i in range(1, 7):
            KS = KS_Op.Updt(KS)
        RK6 = KS_Op.Ext(KS, 6)
        rkT = Tau(RK6)
        rkSt6 = Pi(rkT)
        vec = rkSt6[0, :]
        return vec
