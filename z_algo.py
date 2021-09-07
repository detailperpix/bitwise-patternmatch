"""
z_algo.py
Name: Wirmantono

Contains function for Z algorithm, a linear time pattern matching algorithm
"""


def z_algo(input_str):
    """
    Z-algorithm performs prefix matching in linear time
    The following implementation of algorithm are based on
    Lecture slides provided by the Unit Coordinator for the Algorithms unit
    on my institution.
    Details were omitted to prevent academic integrity issues.

    Time complexity: O(N), N as length of input_str
    Space complexity: O(N) input space
                      O(N) auxiliary space
    """
    def compare(input_str, i, j):
        """
        Performs character by character comparison
        For each iteration compares the suffix of input_str
        with prefix of input_str
        Time complexity: Worst&Best case: O(m); m as length of input_str
        Space complexity: O(m) Input space
        """
        n = len(input_str)
        matches = 0
        while i < n:
            prefix_char = input_str[j]
            suffix_char = input_str[i]
            if prefix_char == suffix_char:
                matches += 1
                i += 1
                j += 1
            else:
                break

        return matches

    # initialize values
    n = len(input_str)
    left = 0
    right = 0

    if n > 0:

        z_values = [0] * n
        z_values[0] = n
    else:
        return []
    # base case
    # skip if input string is only 1
    # get value of Z1
    if (n > 1):
        value_z1 = compare(input_str, 1, 0)
        z_values[1] = value_z1
        if (value_z1 > 0):
            right = value_z1 + 1
            left = 1

    # general case
    for k in range(1, n):
        if k > (right - 1):  # case 1
            value_zk = compare(input_str, k, 0)
            z_values[k] = value_zk
            if (value_zk > 0):
                # calculate position of mismatch
                right = value_zk + k
                left = k
            # else no update is necessary
        else:  # case 2
            # get previous z values
            prev_z = z_values[k - left]  # z_values[k - left + 1]
            remainder = right - k
            if (prev_z < remainder):  # case 2a
                z_values[k] = prev_z
            else:
                if (prev_z > remainder):  # case 2b
                    z_values[k] = remainder
                else:  # case 2c
                    # explicit comparison from right
                    right_compare = compare(input_str, right, right - k)
                    z_values[k] = prev_z + right_compare
                    left = k
                    right = k + right_compare
    return z_values


def bitwise_z_algo(pattern, text):
    """
    creates the first bitvector in len(pattern)
    Concept: run z algo for only 0:len(pattern) of text
    :param pattern:
    :param text:
    :return: z array for text[0:len(pattern)]

    Time complexity: Worst&Best case: O(m); m as length of pattern
    Space complexity: O(m + n); m as length of pattern, n as length of text
                      O(m) auxiliary space
    The algorithm performs pattern matching with Z algorithm
    for pattern. Which will be later be used to a customised z algorithm
    to compute bit vector for the first m character of text, by comparing
    it with pattern.
    """

    def compare(pattern, text, i, j):
        """
        Performs character by character comparison
        For each iteration compares the suffix of text
        with prefix of pattern
        Time complexity: Worst&Best case: O(m); m as length of pattern
        Space complexity: O(pattern + text) Input space
                          O(pattern) Auxiliary space
        """
        m = len(pattern)
        matches = 0
        while i < m:
            prefix_char = pattern[j]
            suffix_char = text[i]
            if prefix_char == suffix_char:
                matches += 1
                i += 1
                j += 1
            else:
                break

        return matches

    n = len(text)
    m = len(pattern)
    left = 0
    right = 0
    z_values = [0] * m
    result = 2 ** m - 1
    z_patt = z_algo(pattern)
    # base case
    # if text is shorter than pattern
    if m > n:
        return result
    if n > 0:
        value_z0 = compare(pattern, text, 0, 0)
        z_values[0] = value_z0
        if value_z0 > 0:
            right = value_z0
            left = 0

    for k in range(1, m):
        if k > right - 1:  # case 1
            value_zk = compare(pattern, text, k, 0)
            z_values[k] = value_zk
            if value_zk > 0:
                # calculate position of mismatch
                right = value_zk + k
                left = k
            # else no update is necessary
        else:  # case 2
            # get previous z values
            prev_z = z_patt[k - left]
            remainder = right - k
            if prev_z < remainder:  # case 2a
                z_values[k] = prev_z
            else:
                if prev_z > remainder:  # case 2b
                    z_values[k] = remainder
                else:  # case 2c
                    # explicit comparison from right
                    right_compare = compare(pattern, text, right, right - k)
                    z_values[k] = prev_z + right_compare
                    left = k
                    right = k + right_compare

    """
    Based on the computation of z_values above, compute the bitvector
    Z_values that is equal to the length of the suffix means that the bitvector
    for the position will be 0.
    """
    for i in range(m):
        if z_values[i] == (m - i):
            result -= 2 ** (m - i - 1)

    return result
