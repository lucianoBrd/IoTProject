# Chiffre de Vigenere
universe = [c for c in (chr(i) for i in range(32,127))]
uni_len = len(universe)
    
def vign(txt='', key='', typ='d'):
    if not txt:
        return 'Needs text.'
    if not key:
        return 'Needs key.'
    if typ not in ('d', 'e'):
        return 'Type must be "d" or "e".'
    if any(t not in universe for t in key):
        return 'Invalid characters in the key. Must only use ASCII symbols.'

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
    
#q = vign('Let\'s check this out!', 'super secret key', 'e')
#print(q)
#print(vign(q, 'super secret key', 'd'))
