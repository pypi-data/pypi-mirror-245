"""
neurotron.cluster.terminal.py:
    class Terminal
"""

from neurotron.math import Attribute, Matrix, Field
from neurotron.cluster.setup import Setup, Plain, Collab, Excite, Predict
from neurotron.math.helper import isa
import neurotron.math as nm

#===============================================================================
# class Terminal
#===============================================================================

class Terminal(Attribute):
    """
    class Terminal:
    >>> collab = Terminal(Collab(3,7,2,5))
    >>> c = Matrix(1,3*7); c[0] = c[1] = c[2] = 1
    >>> collab(c)
    [1 0 0 0 0 0 0; 1 0 0 0 0 0 0; 1 0 0 0 0 0 0]
    >>> excite = Terminal(Plain(3,7))
    >>> excite._simple([1,0,0,1,1])
    [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
    """
    #def __init__(self,K,P=None,eta=0.5,theta=None,delta=(0.1,0.1),verbose=0):
    def __init__(self,setup,eta=None,theta=None,delta=None,verbose=0):
        assert isa(setup,Setup)
        self.eta = setup.eta if eta is None else eta
        self.theta = setup.theta if theta is None else theta
        self.delta = setup.delta if delta is None else delta
        #if isa(K,int) and isa(P,int):
        #    m = K;  n = P
        #    self.shape = (m,n)
        #    self.K = self.P = self.W = self.eta = self.theta = None
        #    return
        self.shape = setup.shape
        self.K,self.P,self.W = setup.get('K,P,W')
        assert self.K is None or isa(self.K,Field)
        assert self.P is None or isa(self.P,Field)
        assert self.W is None or isa(self.W,Field)

        if self.theta is not None and len(self.shape) >= 4:
            theta = self.theta
            self.theta = theta if theta is not None else min(3,self.shape[3])

        #print('### shape:',self.shape,'theta:',self.theta)
        self.verbose = verbose

        if self.K is not None and self.P is not None:
            self.I = Field(*self.K.shape)  #  learning increment
        else:
            self.I = None

    def map(self):
        print('eta:',self.eta,', theta:',self.theta,', delta:',self.delta)
        if self.K is None:
            print('K: None')
        else:
            self.K.map('K: ')
        if self.P is None:
            print('P: None')
        else:
            self.P.map('P: ')
        if self.W is None:
            print('W: None')
        else:
            self.W.map('W: ')

    def weight(self):
        if self.P is not None:
            m,n,d,s = self.K.shape
            for k in range(m*n):
                self.W[k] = self.P[k] >= self.eta
        return self.W

    def empower(self,v):
        m,n,d,s = self.K.shape
        E = Field(m,n,d,s)
        self.weight()               # refresh weight
        for k in range(m*n):
            V = v[self.K[k]]
            E[k] = V * self.W[k]
        return E

    def _simple(self,v):            # simple spiking
        if not isa(v,Matrix): v = Matrix(v)
        S = Matrix(*self.shape)
        m,n = self.shape
        for j in range(min(n,v.shape[1])):
            for i in range(m):
                s = (v[j] > 0);  S[i,j] = s
        return S

    def mind(self,sk,V,k):
        def log(I,k):
            d,s = I.shape
            for ii in range(d):
                if nm.any(I[ii,:]):
                    print('mind I[%g].%g:' % (k,ii), I[ii,:])
        m,n,d,s = self.P.shape
        pdelta,ndelta = self.delta
        S = sk.T @ nm.ones(1,s)
        I = S * (2*pdelta*V - ndelta)
        if self.verbose > 0: log(I,k)
        #if any(sk):
        #    print('##### mind V:',V)
        #    print('#####      S:',S)
        #    print('#####      I:',I)
        return I

    def learn(self,L):
        def log(P,I,k):
            m,n,d,s = P.shape
            for ii in range(d):
                if nm.any(I[k][ii,:]):
                    Pii = P[k][ii,:];  Iii = I[k][ii,:]
                    print('learn P[%g].%g:' % (k,ii),Pii,'by',Iii)
        for k in self.P.range():
            if L[k]:
                self.P[k] = nm.max(0,nm.min(1,self.P[k]+self.I[k]))
                if self.verbose > 0:
                    log(self.P,self.I,k)

    def spike(self,v):              # calculate spike vectors
        if not isa(v,Matrix): v = Matrix(v)
        if self.K is None:
            J = self._simple(v)
            S = Field(*self.shape,1,1)
            for k in S.range(): S[k] = J[k]
            return S
        m,n,d,s = self.K.shape
        if d*s == 0:
            return 0
        S = Field(m,n,1,d)
        self.weight()               # refresh weight
        for k in range(m*n):
            V = v[self.K[k]]
            E = V * self.W[k]
            #print('nm.sum(E.T) >= self.theta:',E,nm.sum(E.T),self.theta)
            S[k] = nm.sum(E.T) >= self.theta
            if self.I is not None:
                self.I[k] = self.mind(S[k],V,k)
        return S

    def clear(self):
        """
        >>> predict = Terminal(Predict(1,3,2,5,rand=True))
        >>> predict.map()
        eta: 0.5 , theta: 3 , delta: (0.1, 0.1)
        K: +-000/0-+-001/1-+-002/2-+
           | 00212 | 12020 | 11100 |
           | 00001 | 02211 | 12110 |
           +-------+-------+-------+
        P: +-000/0-+-001/1-+-002/2-+
           | rkkHH | rPeeE | UheWE |
           | 1UAMA | WwAEU | AwRCm |
           +-------+-------+-------+
        W: +-000/0-+-001/1-+-002/2-+
           | 00011 | 01001 | 10011 |
           | 11111 | 10111 | 10110 |
           +-------+-------+-------+
        >>> predict.clear().map()
        eta: 0.5 , theta: 3 , delta: (0.1, 0.1)
        K: +-000/0-+-001/1-+-002/2-+
           | 00000 | 00000 | 00000 |
           | 00000 | 00000 | 00000 |
           +-------+-------+-------+
        P: +-000/0-+-001/1-+-002/2-+
           | 00000 | 00000 | 00000 |
           | 00000 | 00000 | 00000 |
           +-------+-------+-------+
        W: +-000/0-+-001/1-+-002/2-+
           | 00000 | 00000 | 00000 |
           | 00000 | 00000 | 00000 |
           +-------+-------+-------+
        """
        m,n,d,s = self.K.shape
        zero = nm.zeros(d,s)
        for k in self.K.range():
            self.K[k] = self.W[k] = zero
            if self.P is not None:
                self.P[k] = zero
        return self

    def __call__(self,v):
        if self.K is None: return self._simple(v)

        m,n,d,s = self.K.shape
        if d*s == 0: return Matrix(m,n)

        S = self.spike(v)
        J = Matrix(*S.shape[:2])
        for k in J.range():
            J[k] = max(S[k])
        return J

#===============================================================================
# unit tests
#===============================================================================

class __TestTerminal__:
    def test_construction():
        """
        >>> collab = Terminal(Collab(3,7,2,5))
        >>> collab.map()
        eta: 0.5 , theta: 1 , delta: (0.1, 0.1)
        K: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  12   |  45   |  78   |  AB   |  DE   |  GH   |  JK   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  02   |  35   |  68   |  9B   |  CE   |  FH   |  IK   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  01   |  34   |  67   |  9A   |  CD   |  FG   |  IJ   |
           +-------+-------+-------+-------+-------+-------+-------+
        P: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-------+-------+-------+-------+-------+-------+-------+
        W: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  11   |  11   |  11   |  11   |  11   |  11   |  11   |
           +-------+-------+-------+-------+-------+-------+-------+
        >>> c = Matrix(1,3*7); c[0] = c[1] = c[2] = 1
        >>> collab(c)
        [1 0 0 0 0 0 0; 1 0 0 0 0 0 0; 1 0 0 0 0 0 0]
        """

    def test_simple1():
        """
        >>> excite = Terminal(Plain(3,7))
        >>> excite.map()
        eta: 0.5 , theta: 0 , delta: (0.1, 0.1)
        K: None
        P: None
        W: None
        >>> excite._simple([1,0,0,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite([1,0,0,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite.spike([1,0,0,1,1]).map()
        +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-------+-------+-------+-------+-------+-------+-------+
        """

    def test_simple2():
        """
        >>> excite = Terminal(Plain(3,7))
        >>> excite.map()
        eta: 0.5 , theta: 0 , delta: (0.1, 0.1)
        K: None
        P: None
        W: None
        >>> excite._simple([1,0,0,1,1,0,0,1,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite([1,0,0,1,1,0,0,1,1,1])
        [1 0 0 1 1 0 0; 1 0 0 1 1 0 0; 1 0 0 1 1 0 0]
        >>> excite.spike([1,0,0,1,1,0,0,1,1,1]).map()
        +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
        |   1   |   0   |   0   |   1   |   1   |   0   |   0   |
        +-------+-------+-------+-------+-------+-------+-------+
        """

    def test_predict():
        """
        >>> nm.seed(0); predict = Terminal(Predict(3,7,2,5,rand=True))
        >>> predict.map()
        eta: 0.5 , theta: 3 , delta: (0.1, 0.1)
        K: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           | CF033 | 79JI4 | 6C167 | EH5D8 | 9KJGJ | 5FF0I | 3HJJJ |
           | E7019 | 0AK3B | I2004 | 568KH | F49A1 | 17936 | BEI0E |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           | 3CAKB | 464FK | 3C4K8 | EFK3F | DGH59 | 3050H | I42G3 |
           | 2ADG7 | 90AIB | 2233I | E3KHI | E914A | B8B2J | G006J |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           | EAJ8D | 232BD | G88J8 | 2K3CE | 043DB | DDBGE | GJ180 |
           | 46D7F | 9I8FB | 6F1C3 | IF3AC | 635B0 | B8KAB | 5F82J |
           +-------+-------+-------+-------+-------+-------+-------+
        P: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           | 1Mppe | AAApM | WHpAC | JeeuH | rrukc | mwErk | RcuUR |
           | pcmRp | epWUu | WUrkk | HHrPe | eEUhe | WE1UA | MAWwA |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           | EUAwR | Cmp1c | Mw1ce | JUwEm | wCMWm | p1ecJ | kwcPP |
           | EmeJC | MU1pA | Wr1EW | JuhCR | RpUCA | HJhhe | cJeRP |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           | cphUe | rRWJm | mHUuk | u11eA | UAw1m | URpCu | mmRRP |
           | CJcEh | APp1H | WUCru | EpHmu | Uwemp | khprc | umwJ1 |
           +-------+-------+-------+-------+-------+-------+-------+
        W: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           | 11000 | 11101 | 11011 | 10001 | 00000 | 00100 | 10011 |
           | 00010 | 00110 | 11000 | 11010 | 01100 | 11111 | 11101 |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           | 11101 | 10010 | 10100 | 11010 | 01110 | 01001 | 00011 |
           | 10011 | 11101 | 10111 | 10011 | 10111 | 11000 | 01011 |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           | 00010 | 01110 | 01100 | 01101 | 11010 | 11010 | 00111 |
           | 11010 | 11011 | 11100 | 10100 | 10000 | 00000 | 00011 |
           +-------+-------+-------+-------+-------+-------+-------+
        >>> c = nm.row([1,0,0,1,1,0,0],nm.ones(1,20))
        >>> predict(c)
        [0 1 0 0 0 1 1; 1 1 1 1 1 0 0; 0 1 0 1 1 1 0]
        >>> predict.spike(c).map('S: ')
        S: +-000/0-+-003/3-+-006/6-+-009/9-+-012/C-+-015/F-+-018/I-+
           |  00   |  10   |  00   |  00   |  00   |  01   |  11   |
           +-001/1-+-004/4-+-007/7-+-010/A-+-013/D-+-016/G-+-019/J-+
           |  10   |  01   |  01   |  11   |  01   |  00   |  00   |
           +-002/2-+-005/5-+-008/8-+-011/B-+-014/E-+-017/H-+-020/K-+
           |  00   |  01   |  00   |  10   |  10   |  10   |  00   |
           +-------+-------+-------+-------+-------+-------+-------+
        """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
