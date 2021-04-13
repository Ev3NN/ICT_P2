import string

L = 7

def lz77(s_buffer, la_buffer):
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

def main():
    search_buffer = [' ' for i in range(L)]
    look_ahead_buffer = list('abracadabrad')
    codewords = []

    while look_ahead_buffer:
        code = lz77(''.join(search_buffer), ''.join(look_ahead_buffer))
        codewords.append(code)

        l = code[1]
        look_ahead_buffer, prefix = look_ahead_buffer[l+1:], look_ahead_buffer[0:l+1]
        search_buffer += prefix

        search_buffer = search_buffer[-L:]

        print('Search: ', search_buffer)
        print('LA: ', look_ahead_buffer)
        print('Code: ', code)

    print('--------------- DONE ---------------')
    print(codewords)
    print(search_buffer)

if __name__ == "__main__":
    main()