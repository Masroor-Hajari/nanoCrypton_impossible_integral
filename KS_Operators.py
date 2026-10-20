import numpy as np
from Basic import CrumbXOR, Int2Crumb
from RF_Operators import SBOX

"""
Instruction:
- KS_Operators.py - key-schedule implementation for the 48-bit nanoCrypton block cipher.
- All inputs and outputs use numpy types:
    - Blocks: numpy with shape (4, 4) and dtype=np.uint8 for each crumb.
    - Single nibble values: numpy scalar or 0-dim numpy array with dtype=np.uint8 (e.g. np.uint8(6) or np.array(6, dtype=np.uint8)).
    - Round/index parameters: plain Python int.
- Functions check input types and values, printing error messages on invalid input and may return None; callers should validate inputs and/or catch exceptions and not rely on printed output for control flow.
"""

###################################################################################################
####                                     Updating process                                      ####
###################################################################################################
def Updt(KS: np.uint8) -> np.uint8:
    try:
        m, n = KS.shape
        if m != 4 or n != 4:
            raise ValueError("Input must be a 4x4 matrix.")
        else:
            updtKS = KS.copy()
            for i in range(0, 3):
                for j in range (0, 4):
                    updtKS[i][j] = KS[(i + 1)][j]
            for i in range(0, 4):
                index = (i + 1) % 4
                b0 = KS[0][i] % 2
                B2 = Int2Crumb(KS[0][index])
                k = b0 * 4 + B2[0] * 2 + B2[1]
                updtKS[3][i] = k
            return updtKS.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                                    Extracting process                                     ####
###################################################################################################
def Ext(KS: np.uint8, r: int) -> np.uint8:
    try:
        m, n = KS.shape
        if type(r) != int or r < 0 or r > 12:
            raise TypeError("The second input must be an integer between 0 and 12.")
        elif m != 4 or n != 4:
            raise ValueError("The first input must be a 4x4 matrix of nibbles.")
        else:
            RC = np.array([1, 2, 4, 5, 7, 3, 6, 3, 7, 5, 4, 2, 1], dtype = np.uint8)
            RK = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range (0, 4):
                    RK[i][j] = KS[(i + 1) % 4][j]
                outNum = SBOX(KS[0][i], 0)
                RK[i][i] = CrumbXOR(RK[i][i], outNum)
                RK[i][i] = CrumbXOR(RK[i][i], RC[r])
            return RK.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)



