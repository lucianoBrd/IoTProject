# Chiffre de Vigenere

# Cant take all char => memory error
# Take char we use + others
universe = [' ', '_', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '{', '}', 'x']
uni_len = len(universe)
    
def vign(txt='', key='', typ='d'):
    if not txt:
        # 'Needs text.'
        return None
    if not key:
        #'Needs key.'
        return None
    if typ not in ('d', 'e'):
        #'Type must be "d" or "e".'
        return None
    if any(t not in universe for t in key):
        #'Invalid characters in the key. Must only use ASCII symbols.'
        return None

    ret_txt = ''
    k_len = len(key)

    for i, l in enumerate(txt):
        if l not in universe:
            ret_txt += l
        else:
            txt_idx = universe.index(l)

            k = key[i % k_len]
            key_idx = universe.index(k)
            if typ == 'd':
                key_idx *= -1

            code = universe[(txt_idx + key_idx) % uni_len]

            ret_txt += code

    return ret_txt

# Exemples of use :
#q = vign('CHLIB_REQUEST', '0x12345678', 'e')
#print(q)
#print(vign(q, '0x12345678', 'd'))
