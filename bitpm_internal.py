"""
bitpm_internal.py
Name: Wirmantono

Provides bitwise pattern matching function for bitpm.py
"""
from z_algo import bitwise_z_algo

CHAR_RANGE = ord('~') - ord(' ') + 1


def create_delta_array(pattern):
    """
    Creates an array of information for delta
    towards the string pattern
    :return: array containing delta values for the pattern
    Time Complexity: O(N); N as length of pattern
    Space complexity: O(N); N as length of pattern
    O(N) input space
    O(1) auxiliary space (the delta_array has a constant size from list of
    95 elements)
    """
    delta_array = [None] * (CHAR_RANGE + 1)
    delta_array[CHAR_RANGE] = (2 ** len(pattern)) - 1

    """
    Determine delta for cases of each characters from ' ' to '~'
    Fills in the character that matches pattern's character
    by updating the values in the delta_array
    i.e. pattern=abcd, delta array for character 'a' would be 0b0111
    (character 'a' matches), character 'c' would be 0b1101
    """
    for i in range(len(pattern)):
        position = ord(pattern[i]) - ord(' ')
        if delta_array[position] is None:
            delta_array[position] = delta_array[CHAR_RANGE]
            delta_array[position] -= 2 ** i
        else:
            delta_array[position] -= 2 ** i

    return delta_array


def bitpm(text, pattern):
    """
    Performs bitwise pattern matching for finding pattern
    in text. The pattern matching takes advantage of the relation
    between bitvector values and Delta vector to perform pattern matching.
    Text that matches will have bit value of 0 in the position of len(pattern).

    Time complexity: O(m+n); m as length of pattern, n as length of text
    Space complexity: O(m+n); m as length of pattern, n as length of text
                      O(m+n) input space
                      O(m) auxiliary space

    Cost of O(m+n) from bitwise_z_algo(), and iterating through the entire text
    costs O(n). Resulting in overall complexity of O(m+n)
    """
    result = []

    if len(pattern) == 0:
        return result

    """
    Preprocessing
    Creates delta array of the pattern for all possible characters
    see create_delta_array()
    """
    delta_array = create_delta_array(pattern)

    """
    Obtain the bit vector for first possible match
    see z_algo.py/bitwise_z_algo()
    """
    bit_vector = bitwise_z_algo(pattern, text)

    for i in range(len(pattern) - 1, len(text)):
        """
        check if bit vector has 0 in the most significant bit
        Most significant bit denotes the 
        """
        if (bit_vector & 2 ** (len(pattern) - 1)) == 0:
            result += [i - len(pattern) + 1]
        # prepare for next comparison
        if i < len(text) - 1:
            """
            Find successor for bit_vector by applying the formula:
            bit_vector(n+1) = bit_vector(n) << 1 || delta(n + 1)
            Performs bitwise 'and' operation to reduce the likelihood of
            integer overflow
            """
            current_delta = delta_array[ord(text[i + 1]) - ord(' ')]
            # if delta(n+1) is empty assume no matches
            if current_delta is None:
                current_delta = delta_array[CHAR_RANGE]

            bit_vector = ((bit_vector << 1) | current_delta) \
                         & 2 ** (len(pattern)) - 1

    return result
