"""
bitpm.py
Name: Wirmantono

main file for bitpm program.
"""
import sys
from bitpm_internal import bitpm

OUTPUT_FILE = "output_bitpm.txt"
text_file = ""
pattern_file = ""

if __name__ == "__main__":
    """ 
    bitpm.py expects to be passed 2 arguments:
    - filename for text
    - filename for pattern

    other arguments will be disregarded
    """
    if len(sys.argv) != 3:
        print("Incorrect usage of bitpm.py, please provide text file and pattern file as arguments.")
        exit()

    text_file = sys.argv[1]
    pattern_file = sys.argv[2]

    # read text and pattern
    with open(text_file, "r") as f:
        text = f.readline()

    with open(pattern_file, "r") as f:
        pattern = f.readline()

    """
    Perform bitwise pattern matching
    see bitpm_internal.py
    """
    result = bitpm(text, pattern)

    # write results to output
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join([str(item) for item in result]))