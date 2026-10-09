import numpy as np
import Basic as Bsc
import RF_Operators as RF_Op
import KS_Operators as KS_Op
import Encryption as Enc

def main():
    A = np.array([[1, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]], dtype = np.uint8)
    B = Enc.Enc(A, A, 12)
    print("...")
    print(B)

if __name__ == "__main__":
    main()
