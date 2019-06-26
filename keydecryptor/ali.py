# -*- coding: utf-8 -*-
'''
Note:
This decryption code is basing on the JS version from 阿里云大学
Example:
se = "a".charCodeAt(0)
ue = function(t) {
    var e = void 0;
    if (20 === t.byteLength) {
        e = new DataView(t,0);
        var r = e.getUint8(0)
            , i = String.fromCharCode(r).toLowerCase()
            , a = parseInt(i, 36) % 7
            , n = e.getUint8(a)
            , o = String.fromCharCode(n)
            , s = e.getUint8(a + 1)
            , l = String.fromCharCode(s)
            , u = parseInt("" + o + l, 36) % 3;
        if (2 === u) {
            var d = e.getUint8(8)
                , h = e.getUint8(9)
                , c = e.getUint8(10)
                , f = e.getUint8(11)
                , p = e.getUint8(15)
                , g = e.getUint8(16)
                , v = e.getUint8(17)
                , y = e.getUint8(18)
                , m = d - se + 26 * (parseInt(String.fromCharCode(h), 10) + 1) - se
                , b = c - se + 26 * (parseInt(String.fromCharCode(f), 10) + 1) - se
                , E = p - se + 26 * (parseInt(String.fromCharCode(g), 10) + 1) - se
                , T = v - se + 26 * (parseInt(String.fromCharCode(y), 10) + 2) - se;
            e = new DataView(new Uint8Array([e.getUint8(0), e.getUint8(1), e.getUint8(2), e.getUint8(3), e.getUint8(4), e.getUint8(5), e.getUint8(6), e.getUint8(7), m, b, e.getUint8(12), e.getUint8(13), e.getUint8(14), E, T, e.getUint8(19)]).buffer)
        } else if (1 === u) {
            var R = new Uint8Array(le(e, "0-1-2-3-4-5-6-7-18-16-15-13-12-11-10-8"));
            e = new DataView(R.buffer)
        } else {
            if (0 !== u)
                return;
            var A = new Uint8Array(le(e, "0-1-2-3-4-5-6-7-8-10-11-12-14-15-16-18"));
            e = new DataView(A.buffer)
        }
    } else if (17 === t.byteLength) {
        e = new DataView(t,1);
        var S = new Uint8Array(le(e, "8-9-2-3-4-5-6-7-0-1-10-11-12-13-14-15"));
        e = new DataView(S.buffer)
    } else
        e = new DataView(t);
    return e
}

le = function(t, e) {
    var r = [];
    return e.split("-").map(
        function(e) {
            r.push(t.getUint8(parseInt(e)))
        }), r
}
'''

class AliKeyDecryptor(object):
    def decrypt(self, key):
        result = None
        se = ord("a")
        if(len(key) == 20):
            r = key[0]
            i = chr(r).lower()
            a = int(i, base=36) % 7
            # n = key[a]
            # o = chr(n)
            # s = key[a+1]
            # l = chr(s)
            # u = int(o+l, base=36) % 3 # equal to 36*o + l, only consider "l" is enough
            s = key[a + 1]
            l = chr(s)
            u = int(l, base=36) % 3
            if(u == 2):
                d = key[8]
                h = key[9]
                c = key[10]
                f = key[11]
                p = key[15]
                g = key[16]
                v = key[17]
                y = key[18]
                m = d - se + 26 * (int(chr(h)) + 1) - se
                b = c - se + 26 * (int(chr(f)) + 1) - se
                E = p - se + 26 * (int(chr(g)) + 1) - se
                T = v - se + 26 * (int(chr(y)) + 2) - se
                #result = str(key[0]) + str(key[1]) + str(key[2]) + str(key[3]) + str(key[4]) + str(key[5]) + str(key[6]) + str(key[7]) + str(m) + str(b) + str(key[12]) + str(key[13]) + str(key[14]) + str(E) + str(T) + str(key[19])
                result = []
                result.append(key[0])
                result.append(key[1])
                result.append(key[2])
                result.append(key[3])
                result.append(key[4])
                result.append(key[5])
                result.append(key[6])
                result.append(key[7])
                result.append(m)
                result.append(b)
                result.append(key[12])
                result.append(key[13])
                result.append(key[14])
                result.append(E)
                result.append(T)
                result.append(key[19])
            elif(u == 1):
                result = []
                result.append(key[0])
                result.append(key[1])
                result.append(key[2])
                result.append(key[3])
                result.append(key[4])
                result.append(key[5])
                result.append(key[6])
                result.append(key[7])
                result.append(key[18])
                result.append(key[16])
                result.append(key[15])
                result.append(key[13])
                result.append(key[12])
                result.append(key[11])
                result.append(key[10])
                result.append(key[8])
            else:
                # u == 0
                result = []
                result.append(key[0])
                result.append(key[1])
                result.append(key[2])
                result.append(key[3])
                result.append(key[4])
                result.append(key[5])
                result.append(key[6])
                result.append(key[7])
                result.append(key[8])
                result.append(key[10])
                result.append(key[11])
                result.append(key[12])
                result.append(key[14])
                result.append(key[15])
                result.append(key[16])
                result.append(key[18])
        elif(len(key) == 17):
            key = key[1:]
            result = []
            result.append(key[8])
            result.append(key[9])
            result.append(key[2])
            result.append(key[3])
            result.append(key[4])
            result.append(key[5])
            result.append(key[6])
            result.append(key[7])
            result.append(key[0])
            result.append(key[1])
            result.append(key[10])
            result.append(key[11])
            result.append(key[12])
            result.append(key[13])
            result.append(key[14])
            result.append(key[15])
        else:
            result = key

        if(type(result) == list):
            result = bytes(result)

        return result
