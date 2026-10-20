import ODTM
import ADTM

def main():
    text = "C:\\PythonRepos\\nanoCrypton_impossible_integral\\PythonApplication1\\PythonApplication1"
    ptxList = ADTM.ADTM_Generate(text)
    ODTM.ODTM_Generate(text)
    ctxList = ADTM.ReadDoc(text)
    hashTable0 = ADTM.PreComp(5, 0)
    whitekeyList0 = ADTM.PartDec(hashTable0, ctxList, 0)
    hashTable1 = ADTM.PreComp(5, 1)
    whitekeyList1 = ADTM.PartDec(hashTable1, ctxList, 1)
    hashTable2 = ADTM.PreComp(5, 2)
    whitekeyList2 = ADTM.PartDec(hashTable2, ctxList, 2)
    hashTable3 = ADTM.PreComp(5, 3)
    whitekeyList3 = ADTM.PartDec(hashTable3, ctxList, 3)
    masterkeylist0 = ADTM.WK2MK(whitekeyList0)
    masterkeylist1 = ADTM.WK2MK(whitekeyList1)
    masterkeylist2 = ADTM.WK2MK(whitekeyList2)
    masterkeylist3 = ADTM.WK2MK(whitekeyList3)
    ptxVec = []
    ptxVec.append(ptxList[0].copy())
    ptxVec.append(ptxList[1].copy())
    ctxVec = []
    ctxVec.append(ctxList[0].copy())
    ctxVec.append(ctxList[1].copy())
    ADTM.Search(ptxVec, ctxVec, masterkeylist0, masterkeylist1, masterkeylist2, masterkeylist3)

if __name__ == "__main__":
    main()