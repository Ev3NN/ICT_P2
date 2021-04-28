import string

L = 3

def compute_codeword(s_buffer, la_buffer):
    """
    Finds the longest prefix in la_buffer that begins in s_buffer,
    and computes the appropriate codeword (d, l, c)

    Parameters
    ----------
    s_buffer: str
        Search buffer containing the past occurrences of
        the message.
    la_buffer: str
        Look-Ahead Buffer containing (a part of) the message
        to encode.
    """
    prefix = la_buffer[0]
    codeword = [0, 0, prefix]
    
    while (idx := s_buffer.rfind(prefix)) != -1:
        d = L - idx
        l = len(prefix)

        if len(prefix) < len(la_buffer):
            c = la_buffer[l]
            codeword = [d, l, c]
            prefix = la_buffer[0:l+1]
        else:
            c = ''
            codeword = [d, l, c]
            break
    
    return tuple(codeword)

def lz77(s_buffer, la_buffer):
    """
    Encodes a sequence using the LZ77 Algorithm. 

    Parameters
    ----------
    s_buffer: str
        Search buffer containing the past occurrences of
        the message.
    la_buffer: str
        Look-Ahead Buffer containing (a part of) the message
        to encode.
    """
    codewords = []
    while la_buffer:
        code = compute_codeword(s_buffer, la_buffer)
        codewords.append(code)

        l = code[1]
        la_buffer, prefix = la_buffer[l+1:], la_buffer[0:l+1]
        s_buffer += prefix

        s_buffer = s_buffer[-L:]
    
    return codewords

def main():
    search_buffer = ' ' * L
    look_ahead_buffer = 'abracadabrad'

    codewords = lz77(search_buffer, look_ahead_buffer)

    print(codewords)

if __name__ == "__main__":
    main()