import ODTM
import ADTM
from Basic import AddressModifiy

"""
Instruction:
- MainDriver.py — orchestrates applying impossible-integral cryptanalysis applied on 6-round 48-bit nanoCrypton.

Purpose and high-level flow:
  In the scenario of nanoCrypton key-recovery using impossible integral cryptanalysis:
   1. Ask the user for a target folder path (Address).
   2. Call ADTM.ADTM_Write(Address) to generate and save plaintext pairs for impossible-integral cryptanalysis.
   3. Receive the corresponding ciphertext pairs from the ODTM and then start seiving the keys by using impossible-integral property.
   4. At the last step by applyng the exhaustive search on remaining-key sets the master key of the algorithm will be recovered.

Types and input expectations:
- Address: plain Python string containing the target folder path. Current implementation concatenates
  a Windows backslash ("\\") internally when forming filenames. For cross-platform usage or to avoid
  double separators, pass an absolute folder path or modify modules to use os.path.join before calling.

User interaction and validation:
- main(Address: str) validates Address is a str and uses input(...) to request pr.
- The pr prompt expects a valid float; the loop re-prompts on invalid values.

Side effects and files created/consumed:
- Plaintexts.txt (written by DDTM.WriteDoc) — file format: each line "0x" + 12 hex chars (row-major).
- Ciphertexts.txt (written by CDTM.WriteDoc) — same format as above.
- Both files are created under the provided Address folder (Address + "\\Plaintexts.txt" / "\\Ciphertexts.txt").

Error handling and robustness:
- main() catches TypeError for an invalid Address argument and prints an error message.
- The called modules (DDTM, CDTM, Encryption, Basic, RF_Operators, KS_Operators) perform their own
  type/dtype checks and typically print error messages on invalid input (often returning None).
  For robust automation, validate and pre-convert inputs (numpy dtypes) before calling or refactor
  helper functions to raise exceptions instead of printing.
- Because file I/O and generation can be expensive, consider:
    - Ensuring the target folder exists and is writable before starting.
    - Running the heavy generation steps in a background thread/process or with progress persistence.
    - Using streaming writes/reads to avoid building huge in-memory lists.

Recommendations and improvements:
- Use os.path.join(Address, "Plaintexts.txt") and os.path.join(Address, "Ciphertexts.txt") inside
  DDTM/CDTM to be cross-platform and avoid path concatenation bugs.
- Convert and validate inputs to numpy types where required by helper modules (e.g. np.uint8).
- Consider returning status codes from main (int) instead of only printing, to support automation.
- Add an optional non-interactive API (pass pr as parameter or via CLI arguments) for scripted runs.
- Add logging instead of prints for better control of verbosity and progress tracking.

Example usage (interactive):
    $ python MainDriver.py
    Please enter the address of the target folder: C:\data\nanoCrypton
    For key recovery scenario the only the address of chosen plaintexts and correspondig ciphertexts shall entered.

Behavior summary:
- main(Address) returns None; primary outputs are created files and console messages.
- For nanoCrypton key recovery the ADTM.ADTM_Write insert the chosen plaintexts and also sieves the possible keys, and ODTM encrypts the required plaintexts using the master key entered in Masterkey.txt file.
"""

def main():
    Address = input("Please enter the address of the target folder: \n")
    text = AddressModifiy(Address)
    ptxList = ADTM.ADTM_Generate(text)
    ODTM.ODTM_Generate(text)
    ctxList = ADTM.ReadDoc(text)
    hashTable0 = ADTM.PreComp(5, 0)
    whitekeyList0 = ADTM.PartDec(text, hashTable0, ctxList, 0)
    hashTable1 = ADTM.PreComp(5, 1)
    whitekeyList1 = ADTM.PartDec(text, hashTable1, ctxList, 1)
    hashTable2 = ADTM.PreComp(5, 2)
    whitekeyList2 = ADTM.PartDec(text, hashTable2, ctxList, 2)
    hashTable3 = ADTM.PreComp(5, 3)
    whitekeyList3 = ADTM.PartDec(text, hashTable3, ctxList, 3)
    masterkeylist0 = ADTM.WK2MK(whitekeyList0, 0)
    masterkeylist1 = ADTM.WK2MK(whitekeyList1, 1)
    masterkeylist2 = ADTM.WK2MK(whitekeyList2, 2)
    masterkeylist3 = ADTM.WK2MK(whitekeyList3, 3)
    ptxVec = []
    ptxVec.append(ptxList[0].copy())
    ptxVec.append(ptxList[1].copy())
    ctxVec = []
    ctxVec.append(ctxList[0].copy())
    ctxVec.append(ctxList[1].copy())
    ADTM.Search(ptxVec, ctxVec, masterkeylist0, masterkeylist1, masterkeylist2, masterkeylist3)

if __name__ == "__main__":
    main()