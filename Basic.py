import numpy as np

"""
Instruction:
- This module provides utilities for the 32-bit block cipher "nanoCrypton" and its operations.

- Key, plaintexts, ciphertexts and intermediate blocks are represented as 4x4 matrices of 2-bit crumbs, where each crumbs is an integer between 0 and 3.

- Pass values using the types annotated on each function (e.g., np.uint8 to represent each crumb of the 4x4 block matrix,
  Python int for RandInt bounds). Convert/validate inputs before calling.

- Callers should catch exceptions raised by these functions; do not rely on printed error messages
  for control flow.
"""

###################################################################################################
####                    Convert an integer to the corresponding 2-bit crumb                    ####
###################################################################################################
def Int2Crumb(n: np.uint8) -> np.uint8:
    try:
        if n.dtype != np.uint8:
            raise TypeError(f"Input must be an integer value.")
        elif n < 0 or n > 3:
            raise ValueError(f"Input must be an integer value between 0 and 3.")
        else:
            B = np.array([0, 0], dtype = np.uint8)
            B[1] = np.uint8(n % 2)
            B[0] = np.uint8(n // 2)
            return B.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                The integer represtentation of the XOR result of two crumbs                ####
###################################################################################################
def CrumbXOR(x: np.uint8, y: np.uint8) -> np.uint8:
    try:
        if x.dtype != np.uint8 or y.dtype != np.uint8:
            raise TypeError(f"Inputs must be integer values.")
        elif x < 0 or x > 3 or y < 0 or y > 3:
            raise ValueError(f"Inputs must be integer values between 0 and 3.")
        else:
            XOR = np.array([[0, 1, 2, 3],
                            [1, 0, 3, 2],
                            [2, 3, 0, 1],
                            [3, 2, 1, 0]], dtype = np.uint8)
            z = XOR[x][y]
            return z.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                   Convert an integer to the corresponding 4-bit nibble                    ####
###################################################################################################
def Int2Nib(n: np.uint8) -> np.uint8:
    try:
        if n.dtype != np.uint8:
            raise TypeError("Input must be an integer number.")
        elif n > 16 or n < 0:
            raise ValueError("In put must be a positive number between 0 and 15.")
        else:
            num3 = n % 2
            temp = (n - num3) // 2
            num2 = temp % 2
            temp = (temp - num2) // 2
            num1 = temp % 2
            num0 = (temp - num1) // 2
            B = np.array([num0, num1, num2, num3])
            return B.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input vlaue.", e2)

###################################################################################################
####                  The integer represtentation of a hexadecimal character                   ####
###################################################################################################
def Hex2Int(x: str) -> np.uint8:
    try:
        if type(x) != str:
            raise TypeError(f"Input must be a hexadecimal string.")
        elif len(x) != 1 or x not in "0123456789abcdefABCDEF":
            raise ValueError(f"Input must be a hexadecimal string of length 1.")
        else:
            y = int(x, 16)
            y = np.array([y], dtype = np.uint8)
            return y.astype(np.uint8)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)
    
###################################################################################################
####                        The hexadecimal represtation of an integer                         ####
###################################################################################################
def Int2Hex(x: np.uint8) -> str:
    try:
        if x.dtype != np.uint8:
            raise TypeError(f"Input must be an integer number.")
        elif x < 0 or x > 15:
            raise ValueError(f"Input must be an integer between 0 and 15.")
        else:
            if x < 10:
                y = chr(x + 48)
            else:
                y = chr(x + 87)
            return y

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                                  Random integer genrator                                  ####
###################################################################################################
def RandInt(a: int, b: int, inclusive: bool) -> np.uint8:
    try:
        if type(a) != int or type(b) != int or type(inclusive) != bool:
            raise TypeError("Bounds must be integers. The thitd parameter must be a boolean value.")
        if a > b:
            raise ValueError("The lower bound must be less than or equal to the upper bound.")
        else:
            rng = np.random.default_rng()
        if inclusive:
            y = rng.integers(a, b + 1)
            return y.astype(np.uint8)
        else:
            try:
                if a == b and inclusive == False:
                    raise ValueError("The lower and upper bounds must be different when the range is exclusive.")
                else:
                    y = rng.integers(a, b)
                    return y.astype(np.uint8)

            except ValueError as e3:
                print("Error: Invalid input.", e3)

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input.", e2)

###################################################################################################
####                               Random integer list genrator                                ####
###################################################################################################
def RndList(upBound: int, N: int) -> list:
    try:
        if type(upBound) != int or type(N) != int:
            raise TypeError("Two inputs must be a non-negative integer numbers.")
        elif upBound < N:
            raise ValueError("number of required random numbers must be less than upper bound.")
        else:
            mid = (upBound - 1) // 2
            if N <= mid:
                bl = True
            else:
                bl = False
                N = upBound - N
                totalList = []
                for i in range(0, upBound):
                    totalList.append(i)
            ctr = 0
            randomList = []
            while ctr < N:
                rng = np.random.default_rng()
                rand = rng.integers(0, upBound)
                if ctr == 0:
                    randomList.append(int(rand))
                    ctr += 1
                else:
                    bl2 = False
                    for i in range(0, ctr):
                        if rand == randomList[i]:
                            bl2 = True
                            break
                    if bl2 == False:
                        randomList.append(int(rand))
                        ctr += 1
            if bl == False:
                totalSet = set(totalList)
                randomSet = set(randomList)
                randomDiffSet = totalSet - randomSet
                randomList = list(randomDiffSet)
            return randomList

    except TypeError as e1:
        print("Error: Invalid input.", e1)

    except ValueError as e2:
        print("Error: Invalid input vlaue.", e2)


###################################################################################################
####                                   Address modification                                    ####
###################################################################################################
def AddressModifiy(Address: str) -> str:
    try:
        if type(Address) != str:
            raise TypeError("Invalid address.")
        else:
            Address.replace("\\", "\\\\")
            modifyAddress = Address
            return modifyAddress

    except TypeError as e:
        print("Error: Invalid input.", e)




