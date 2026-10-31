"""Small dependency-free XXH32 implementation for game string-key lookup.
Algorithm reference: https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash_spec.md
This does not decrypt or modify any assets; it matches already exported table keys.
"""
MASK = 0xffffffff
P1, P2, P3, P4, P5 = 2654435761, 2246822519, 3266489917, 668265263, 374761393

def rot(x, n):
    return ((x << n) | (x >> (32-n))) & MASK

def xxh32(data, seed=0):
    data = bytes(data)
    n, pos = len(data), 0
    if n >= 16:
        v = [(seed+P1+P2)&MASK, (seed+P2)&MASK, seed&MASK, (seed-P1)&MASK]
        while pos <= n-16:
            for j in range(4):
                word = int.from_bytes(data[pos:pos+4], "little"); pos += 4
                v[j] = (rot((v[j] + word*P2)&MASK, 13)*P1)&MASK
        h = (rot(v[0],1)+rot(v[1],7)+rot(v[2],12)+rot(v[3],18))&MASK
    else:
        h = (seed+P5)&MASK
    h = (h+n)&MASK
    while pos <= n-4:
        h = (rot((h+int.from_bytes(data[pos:pos+4],"little")*P3)&MASK,17)*P4)&MASK
        pos += 4
    while pos < n:
        h = (rot((h+data[pos]*P5)&MASK,11)*P1)&MASK;pos+=1
    h ^= h >> 15; h = (h*P2)&MASK
    h ^= h >> 13; h = (h*P3)&MASK
    return (h ^ (h >> 16))&MASK
