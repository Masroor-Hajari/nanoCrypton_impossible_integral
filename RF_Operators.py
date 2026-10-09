import numpy as np
from Basic import Int2Crumb, CrumbXOR

"""
Instruction:
- This module implements round-function operators for 32-bit blocks for nanoCrypton blockcipher.
- Use numpy types: pass blocks as numpy.ndarray with shape (4,4) and dtype=np.uint8.
- Functions check .dtype and .shape; plain Python ints/lists will cause TypeError. Convert inputs before calling: np.uint8(value) or np.array(value, dtype=np.uint8).
- Functions print error messages on invalid input and may return None; callers should validate inputs and/or catch exceptions and not rely on printed output for control flow.
- Returned values are numpy arrays or numpy scalars (dtype=np.uint8). Convert to Python int with int(...) when a native int is required.
"""

###################################################################################################
####                                    nanoCrypton SBOXes                                     ####
###################################################################################################
def SBOX(x: np.uint8, num: int) -> np.uint8:
    try:
        if x.dtype != np.uint8 or type(num) != int:
            raise TypeError("Inputs must be an integer number.")
        elif x < 0 or x > 3 or num < 0 or num > 3:
            raise ValueError("First Input must be between 0 and 3 and second one must be between 0 and 3.")
        else:
            sbox = np.array([[2, 0, 3, 1],
                             [1, 2, 0, 3],
                             [1, 3, 0, 2],
                             [2, 0, 1, 3]], dtype=np.uint8)
            y = sbox[num][x]
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input type.", e1)
    except ValueError as e2:
        print("Error: Invalid input value.", e2)
###################################################################################################
####                                      Gamma operator                                       ####
###################################################################################################
def Gamma(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 3 or X.min() < 0:
            raise ValueError("Each element of the block must be a a value between 0 and 3.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    inNum = X[i][j]
                    num = (i + j) % 4
                    outNum = SBOX(inNum, num)
                    Y[i][j] = outNum
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                  Inverse Gamma operator                                   ####
###################################################################################################
def InvGamma(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 3 or X.min() < 0:
            raise ValueError("Each element of the block must be a a value between 0 and 3.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    inNum = X[i][j]
                    num = (i + j + 2) % 4
                    outNum = SBOX(inNum, num)
                    Y[i][j] = outNum
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                        Pi operator                                        ####
###################################################################################################
def Pi(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 3 or X.min() < 0:
            raise ValueError("Each element of the block must be a a value between 0 and 3.")
        else:
            M = np.array([[0, 1],
                          [1, 0],
                          [1, 1],
                          [1, 1]], dtype = np.uint8)
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    B1 = np.array([0, 0], dtype = np.uint8)
                    for l in range(0, 4):
                        t = (i + j + l) % 4
                        mask = M[t, :].copy()
                        B2 = Int2Crumb(X[l][j])
                        B3 = np.array([0, 0], dtype = np.uint8)
                        B3[0] = np.uint8(B2[0] & mask[0])
                        B3[1] = np.uint8(B2[1] & mask[1])
                        B1[0] = np.uint8(B1[0] ^ B3[0])
                        B1[1] = np.uint8(B1[1] ^ B3[1])
                    Y[i][j] = np.uint8(B1[0] * 2 + B1[1])
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                       Tau operator                                        ####
###################################################################################################
def Tau(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 3 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    Y[i][j] = X[j][i]
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                       Pi* operator                                        ####
###################################################################################################
def PiStar(X: np.uint8) -> np.uint8:
    m, n = X.shape
    try:
        if m != 4 or n != 4:
            raise TypeError("Each block must be a 4x4 matrix of binary values.")
        elif X.max() > 3 or X.min() < 0:
            raise ValueError("Each element of the block must be a binary value.")
        else:
            V = Tau(X)
            W = Pi(V)
            Y = Tau(W)
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)


###################################################################################################
####                                      Sigma operator                                       ####
###################################################################################################
def Sigma(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of binary values.")
        elif X.max() > 3 or X.min() < 0 or K.max() > 3 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            Y = np.array([
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
                ], dtype = np.uint8)
            for i in range(0, 4):
                for j in range(0, 4):
                    Y[i][j] = CrumbXOR(X[i][j], K[i][j])
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                      Sigma* operator                                       ####
###################################################################################################
def SigmaSt(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of binary values.")
        elif X.max() > 3 or X.min() < 0 or K.max() > 3 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            kt = Tau(K)
            kSt = Pi(kt)
            Y = Sigma(X, kSt)
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                      Round function                                       ####
###################################################################################################
def RF(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of binary values.")
        elif X.max() > 3 or X.min() < 0 or K.max() > 3 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            Z = Gamma(X)
            W = Pi(Z)
            V = Tau(W)
            Y = Sigma(V, K)
            return Y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)

###################################################################################################
####                                   Last-Round function                                    #####
###################################################################################################
def LastRF(X: np.uint8, K: np.uint8) -> np.uint8:
    m, n = X.shape
    p, q = K.shape
    try:
        if m != 4 or n != 4 or p != 4 or q != 4:
            raise TypeError("Inputs must be 4x4 matrices of nibbles.")
        elif X.max() > 3 or X.min() < 0 or K.max() > 3 or K.min() < 0:
            raise ValueError("Either input block or input key is not a binary array.")
        else:
            Z = Gamma(X)
            W = SigmaSt(Z, K)
            C = Tau(W)
            return C.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid dimentions.", e1)

    except ValueError as e2:
        print("Error: Invalid input values.", e2)





