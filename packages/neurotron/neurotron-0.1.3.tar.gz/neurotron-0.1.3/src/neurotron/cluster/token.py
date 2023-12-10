"""
module neurotron.cluster.token
    class Token  # deal with tokens
"""

from neurotron.math.matrix import Matrix
from neurotron.math.matfun import SEED as seed, RAND as rand
import neurotron.math.matfun as mf
isa = isinstance

#=========================================================================
# class Token
#=========================================================================

class Token(dict):
    """
    >>> Token()
    Token({})
    >>> Token({'word1':[0,1,0],'word2':[1,0,1]})
    Token({'word1': [0, 1, 0],'word2': [1, 0, 1]})
    >>> token = Token().create(2,4);
    >>> token
    Token({'.': [0, 0, 1, 1]})
    >>> token.range
    (2, 2)
    >>> token.shape
    (1, 4)
    >>> new = token('new'); token
    Token({'.': [0, 0, 1, 1],'new': [0, 1, 0, 1]})
    >>> token.shape
    (2, 4)
    >>> token.null()
    [0, 0, 0, 0]
    """
    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        self._init()
        self.autopimp = False

    def null(self):   # null token
        m,n = self.shape
        return [0 for k in range(n)]

    def pattern(self,list):
        """
        >>> Token().pattern([1,0,1,0])
        '1010'
        """
        str = ''
        for item in list: str += '1' if item else '0'
        return str

    def pimp(self,terminal):
        for key in self:
            code = self.pattern(terminal(self[key]))
            self._decoder[code] = key
            #print('key:',key,'code:',code)

    def _init(self):
        self._decoder = {}  # inverse map's dictionary
        low = 999999999; high = -1
        for key in self:
            bits = self[key]
            pat = self.pattern(bits)
            self._decoder[pat] = key
            n = sum(bits)
            low = min(low,n);  high = max(high,n)
        self.range = (low,high)
        self.shape = self._shape()

    def _shape(self):
        """
        >>> Token().create(3,10)._shape()
        (1, 10)
        """
        #if self == {}: return (0,0)
        m = 0; n = 0
        for key in self:
            n = max(n,len(self[key]));  m += 1
        return (m,n)

    def create(self,m,n):
        """
        >>> Token().create(3,10)
        Token({'.': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]})
        """
        head = [0 for k in range(n-m)]
        tail = [1 for k in range(m)]
        return Token({'.':head+tail})

    def decode(self,arg=None):
        """
        >>> token = Token({'word1':[0,1,0],'word2':[1,0,1]})
        >>> print(token)
        Token({'word1': [0, 1, 0],'word2': [1, 0, 1]})
        >>> token.decode([0,1,0])
        'word1'
        >>> token.decode(Matrix([[1,0,0],[0,0,1]]))
        'word2'
        >>> token.decode([1,1,1])
        ['word1', 'word2']
        >>> token.decode([0,0,0])
        ''
        >>> token.decode('junk')
        ''
        """
        decoder = self._decoder
        if arg is None:
            return decoder
        elif isa(arg,list):
            key = self.pattern(arg)
            return decoder[key] if key in decoder else self._multi(arg)
        elif isa(arg,Matrix):
            #print('arg:',arg)
            if arg.shape[0] > 1:
                arg = mf.MAX(arg)
            row = arg.list()[0]
            key = self.pattern(row)
            #print('### decoder:',decoder)
            #print('###  row:',row,'key:',key,'in decoder:',key in decoder)
            return decoder[key] if key in decoder else self._multi(row)
        else:
            return ''

    def _multi(self,row):
        row = Matrix(row)
        result = []
        for key in self:
            pattern = Matrix(self[key])
            #print('### row:',row,'pattern:',pattern)
            if row.shape == pattern.shape:
                match = mf.AND(row,pattern)
                if all(match==pattern):
                    result.append(key)
        if len(result) == 1: result = result[0]
        return result if result != [] else ''

    def upgrade(self,word):
        """
        >>> token = Token({'word1':[0,1,0,1],'word2':[1,0,1,0]})
        >>> seed(0); token.upgrade('word3')
        [1, 0, 0, 1]
        >>> token.shape
        (3, 4)
        """
        if len(self) == 0: raise Exception('cannot upgrade empty tokenizer')
        key = next(iter(self))        # 1st key
        n = len(self[key])
        zero = [0 for k in range(n)]  # zero token
        low,high = self.range

        for k in range(100000):       # max 100000 trials
            m = low + rand(1+high-low)
            pattern = zero.copy()
            count = 0
            while count < m:          # while not all m bits set
                idx = rand(n)
                if pattern[idx] == 0:
                    pattern[idx] = 1
                    count += 1

                # is this a new pattern?

            found = False
            for key in self:
                if self[key] == pattern:
                    found = True
                    break

            if not found:     # cool - we found a new pattern
                self[word] = pattern

                pat = self.pattern(pattern)
                self._decoder[pat] = word  # refresh decoder
                #print('### update _decoder:',self._decoder)

                m,n = self.shape
                self.shape = (m+1,n)
                return pattern
        raise Exception('gave up after 100k trials')

    def __call__(self,word):
        """
        return token pattern (with auto-upgrade)
        >>> token = Token({'word1':[0,1,0,1],'word2':[1,0,1,0]})
        >>> seed(0); token('word3')
        [1, 0, 0, 1]
        """
        if word in self: return self[word]
        return self.upgrade(word)          # upgrade if not found

    def __str__(self):
       nl = '\n' if len(self) > 2 else ''
       tab = '  ' if len(self) > 2 else ''
       txt = 'Token({' + nl; sep = ''
       for key in self:
           txt += sep + tab + "'%s': " % key + str(self[key])
           sep = ',' + nl
       txt += '})' if len(self) <= 2 else sep + '})'
       return txt

    def __repr__(self):
        return str(self)

#===============================================================================
# class Text
#===============================================================================

class Text:
    """
    access splitted text:
    >>> text = Text('The quick brown fox jumps over the lazy dog',8); text
    Text(12,8,['The quic','quick br','k brown ',...])
    >>> text[2]
    'k brown '
    >>> text(2)
    ['k', ' ', 'b', 'r', 'o', 'w', 'n', ' ']
    >>> text.shape
    (12, 8)
    """
    def __init__(self,text=None,n=None):  # split in m chunks of length n
        if text is None or n is None:
            return
        self.chunks = self._split(text,n)
        self.shape = (len(self.chunks),n)

    def refine(self,raw):  # remove newline characters
        text = ''
        while len(raw) > 0 and (raw[0] == '\n' or raw[0] == ' '):
            raw = raw[1:]
        for c in raw:
            text += c if c != '\n' else ' '
        return text

    def _split(self,text,n):  # first refine then split text
        text = self.refine(text)
        chunks = [];  N = len(text)
        blank = ''.join(' ' for i in range(n))

        off = n//2
        for k in range(len(text)//n+1):
            chunk = text[k*n:min(k*n+n,N)]
            if len(chunk) < n: chunk += blank[:n-len(chunk)]
            chunks.append(chunk)

            chunk = text[k*n+off:min(k*n+off+n,N)]
            if len(chunk) < n: chunk += blank[:n-len(chunk)]
            chunks.append(chunk)
        return chunks

    def __call__(self,idx=None):
        if idx is None: return self.chunks
        list = []
        for c in self.chunks[idx]: list += c
        return list

    def __getitem__(self,idx):
        return self.chunks[idx]

    def __str__(self):
        m,n = self.shape
        more = '['; sep = ''
        for i in range(min(m,3)):
            more += sep + "'" + str(self.chunks[i]) + "'"
            sep = ','
        if m > 3: more += ',...'
        more += ']'
        return 'Text(%g,%g,%s)' % (m,n,more)

    def __repr__(self):
        return self.__str__()

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
