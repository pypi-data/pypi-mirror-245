"""
module neurotron.cluster.trainer
    class Cells    # derived class of Cluster
    class Train    # sequence trainer
    class Trainer  # advanced sequence trainer
"""

from neurotron.cluster.cells import Cluster, Cells, follow
from neurotron.cluster.token import Token
from neurotron.math.matrix import Matrix
from neurotron.cluster.toy import Toy
from neurotron.cluster.monitor import Record, Monitor
import neurotron.math as nm
isa = isinstance

#===============================================================================
# class Train
#===============================================================================

class Train:
    """
    parameter training
    >>> Train()
    Train(Cells(2,5,2,3))
    >>> Train(Cells('Mary'))
    Train(Cells('Mary'))
    """
    def __init__(self,cells=None,plot=False,verbose=0):
        self.memory = {}
        self._words = {}
        self._contexts = {}
        self.cells = Cells() if cells is None else cells

        self.learning = True   # learning on the fly during training
        self.plotting = plot
        self.verbose = verbose

    def pattern(self,list):
        """
        >>> Train().pattern([1,0,1,0])
        '1010'
        """
        str = ''
        for item in list: str += '1' if item else '0'
        return str

    def hash(self,M):    # hash of a matrix
        """
        Train().hash(Matrix([[1,1,0],[0,1,1]]))
        """
        list = M.list();  str = ''
        m,n = M.shape; sep = ''
        for i in range(m):
            row = list[i]
            str += sep + self.pattern(row); sep = '|'
        return str

    def next(self,M):
        """
        >>> Train().next(Matrix(2,3))
        [1 1 1; 0 0 0]
        >>> Train().next([[0,1,1],[1,0,0]])
        [1 0 1; 0 1 0]
        >>> Train().next([[0,0,0],[1,1,1]])
        """
        if M is None:
            m,n,d,s = self.cells.shape
            return follow(Matrix(m,n))
        return follow(M)

    def token(self,word=None):
        """
        >>> dict = Train(Cells('Mary')).token()
        >>> Train(Cells('Mary')).token('likes')
        [0, 0, 1, 0, 0, 0, 0, 1, 1]
        """
        if word is None: return self.cells.token
#       return self.cells.token[word]
        return self.cells.token(word)

    def number(self,M):
        m,n = M.shape; nmb = 0; base = 1;
        for j in range(n):
            for i in range(m):
                if M[i,j]:
                    nmb += base*i; break
            base *= m
        return nmb

    def code(self,M):
        m,n = M.shape; code = Matrix(1,n)
        for j in range(n):
            for i in range(m):
                if M[i,j]:
                    code[0,j] = i; break
        return code

    def index(self,token):
        """
        >>> train = Train(Cells('Mary'))
        >>> train.index(train.token('likes'))
        [2, 7, 8]
        """
        idx = []
        for k in range(len(token)):
            if token[k]: idx.append(k)
        return idx

    def learn(self,context,verbose=0,plot=False):
        pass

    def _word(self,word,new):  # store/update word to ._words
        """
        word 'Mary' is stored as ([0,7,8],'#0',[[1,1,1],[0,0,0]])
        >>> Train(Cells('Mary'))._word('Mary',True)
        ('Mary', ([0, 7, 8], '#0', [0 0 0; 0 0 0]))
        """
        m = self.cells.shape[0]
        n = len(self.index(self.token(word)))
        if not word in self._words:
            assert new
            triple = (self.index(self.token(word)),'#0',Matrix(m,n))
            #print('### triple:',triple)
        else:
            assert not new
            triple = self._words[word]
            idx,key,M = triple
            key = '#%g' % (int(key[1:])+1)
            M = self.next(M)
            if M is None:
                raise Exception('representation overflow (max m**n = %g)' % m**n)
            triple = (idx,key,M)
        self._words[word] = triple
        return(word,triple)

    def _train(self,curctx,word,verbose=0,plot=False):
        """
        >>> train = Train(Cells('Mary'))
        >>> ans = train._train('','Mary')
        >>> train._train('<Mary>','likes')
        '<Mary likes>'
        >>> train.show(token=False)
        words:
            Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
            likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        contexts:
            <Mary>:
               #: ([0, 7, 8], '#0', 'Mary')
               @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
               likes: (1, '<Mary likes>', [2, 7, 8])
            <Mary likes>:
               #: ([2, 7, 8], '#1', 'likes')
               @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
        """
        if self.cells.char:
            word = word if word != ' ' else '_'
        if not word in self._words: self._word(word,True)
        if curctx == '':
            newctx = '<' + word + '>'
        else:
            newctx = '<' + curctx[1:-1] + ' ' + word + '>'

            # example: curctx = '<Mary>', word = 'likes'
            #          newctx = '<Mary likes>'

        if not newctx in self._contexts:
            if not curctx == '': self._word(word,False) # next word representation
            triple = self._words[word]
            idx,key,M = triple     # triple = ([2, 7, 8], '#1', [1 1 1; 0 0 0])
            idx = self.index(self.token(word))
            dict = {'#':(idx,key,word)}
            code = self.code(M)
            tag = '';  sep = ''
            for k in range(code.shape[1]):
                tag += sep + '%g.%g' % (idx[k],code[0,k]); sep = '-'
            dict['@'] = [key,M,tag]
            self._contexts[newctx] = dict

        if curctx in self._contexts:
            idx = self.index(self.token(word))
            dict = self._contexts[curctx]
            if word in dict:
                count,value,index = dict[word]
                assert value == newctx
                assert index == idx
            else:
                count = 0
            dict[word] = (count+1,newctx,idx)
            self._contexts[curctx] = dict
        if self.learning:  # learning on the fly during traiing?
            self.learn(curctx,verbose=verbose,plot=plot)
        return newctx

    def _sequence(self,context,sequence,verbose=0,plot=False):
        """
        process sequence:
        >>> train = Train(Cells('Mary'))
        >>> train._sequence('',['Mary','likes'])
        '<Mary likes>'
        """
        for word in sequence:
            context = self._train(context,word,verbose=verbose,plot=plot)
        return context

    def __call__(self,context,arg=None,verbose=None,plot=None):
        """
        >>> train = Train(Cells('Mary'))
        >>> train('','Mary')
        '<Mary>'
        >>> train('Mary')
        '<Mary>'
        >>> train('<Mary>','likes')
        '<Mary likes>'
        >>> train('','Mary likes'.split())
        '<Mary likes>'
        >>> train('Mary likes')
        '<Mary likes>'
        >>> train('Mary likes',5)
        '<Mary likes>'
        """
        if plot is None: plot = self.plotting
        if verbose is None: verbose = self.verbose

        if isa(arg,int):
            sequence = context
            for k in range(arg):
                context = self(sequence,verbose=verbose,plot=plot)
            return context
        if arg is None:
            arg = context.split() if isa(context,str) else context
            context = ''
        if isa(arg,list):
            sequence = arg  # rename
            return self._sequence(context,sequence,verbose=verbose,plot=plot)
        return self._train(context,arg,verbose=verbose,plot=plot)

    def __str__(self):
        if self.cells is None: return 'Train()'
        if self.cells.toy is not None:
            return "Train(Cells('%s'))" % self.cells.toy.tag
        return 'Train(Cells(%g,%g,%g,%g))' % self.cells.shape

    def __repr__(self):
        return self.__str__()

    def show(self,token=True):
        if token:
            print('token:')
            for word in self.cells.token:
                idx = self.index(self.token(word))
                print('   ',idx,'%s:' % word,self.token(word))
        print('words:')
        for word in self._words:
            print('   ','%s:' % word,self._words[word])
        print('contexts:')
        for context in self._contexts:
            dict = self._contexts[context]
            print('   ','%s:' % context)
            for key in dict:
                print('       %s:' % key,dict[key])

#===============================================================================
# class Trainer
#===============================================================================

class Trainer(Train):
    def __init__(self,cells,plot=False,verbose=0):
        super().__init__(cells,verbose=verbose,plot=plot)

    def __call__(self,context,n=None,verbose=None,plot=None):
        return super().__call__(context,n,verbose=verbose,plot=plot)

    def prediction(self,context):
        if context in self._contexts:
            info = self._contexts[context]
            counters = []; total = 0
            for key in info:
                if not key in ['#','@']:
                    n,refer,idx = info[key]
                    total += n
                    counters.append(n)
                    #print('    statistics: %s:' % key,(counters,total))
            result = []; k = 0
            src = self.address(context)
            for key in info:
                if not key in ['#','@']:
                    ratio = counters[k]/total
                    k += 1
                    n,refer,idx = info[key]
                    dst = self.address(refer)
                    result.append((refer,ratio,src,dst))
                    #print('    predict(%g%%): %s ->'%(100*ratio,key),info[key])
            return result

    def predict(self,context):
        results = self.prediction(context)
        for prediction in results:
            refer,ratio,src,dst = prediction
            print('    %g%%: ->' % (100*ratio),refer,src,dst)

    def address(self,context):
        if context in self._contexts:
            info = self._contexts[context]
            m,n,d,s = self.cells.shape
            idx = self.code((info['@'][1])).list()[0];
            jdx = info['#'][0]
            assert len(idx) == len(jdx)
            kdx = [jdx[s]*m+idx[s] for s in range(len(idx))]
            #return ((m,n),idx,jdx,kdx)
            return kdx
        return None

    def learn(self,context,verbose=0,plot=False):
        results = self.prediction(context)
        if results is None: return
        for prediction in results:
            refer,ratio,src,dst = prediction
            if verbose:
                print('    %4.1f%%:' % (100*ratio),context,'->',refer,src,dst)
            self.cells.init()
            for k in dst:
                self.cells.X[k] = 1
            for k in src:
                self.cells.Y[k] = 1

            self.cells.connect(src,dst)
            title = 'learn: ' + refer
            #if self.plotting: self.plot(title)
            if plot: self.plot(title)
            self.cells.init()

    def program(self,verbose=0):   # learn all contexts
        """
        learn all contexts
        >>> train = Trainer(Cells('Mary'))
        >>> train.program()
        """
        for context in self._contexts:
            results = self.prediction(context)
            for prediction in results:
                refer,ratio,src,dst = prediction
                for k in dst:
                    self.cells.X[k] = 1
                for k in src:
                    self.cells.Y[k] = 1
                try:
                    self.cells.connect(src,dst)
                    if verbose:
                        print(Ansi.G + '    learning:',context,'OK'+Ansi.N)
                except SynapseErr:
                    print(Ansi.R+'    learning:',context,'FAIL'+Ansi.N)

    def plot(self,title=''):
        m,n,d,s = self.cells.shape
        mon = Monitor(m,n)
        self.cells.plot(mon,label=True)
        mon.title(title)

    def analyse(self,sentence,all=False):
        if all:
            prediction = self.cells.process(sentence)
        else:
            prediction = self.cells.run(sentence)
            self.plot()
        return prediction

#===============================================================================
# unit tests
#===============================================================================

def test_train():
    """
    >>> train = Train(Cells('Mary'))
    >>> train.show()
    token:
        [0, 7, 8] Mary: [1, 0, 0, 0, 0, 0, 0, 1, 1]
        [1, 7, 8] John: [0, 1, 0, 0, 0, 0, 0, 1, 1]
        [0, 6, 7] Lisa: [1, 0, 0, 0, 0, 0, 1, 1, 0]
        [1, 6, 7] Andy: [0, 1, 0, 0, 0, 0, 1, 1, 0]
        [2, 7, 8] likes: [0, 0, 1, 0, 0, 0, 0, 1, 1]
        [3, 7, 8] to: [0, 0, 0, 1, 0, 0, 0, 1, 1]
        [4, 7, 8] sing: [0, 0, 0, 0, 1, 0, 0, 1, 1]
        [4, 6, 7] dance: [0, 0, 0, 0, 1, 0, 1, 1, 0]
        [5, 7, 8] hike: [0, 0, 0, 0, 0, 1, 0, 1, 1]
        [5, 6, 7] paint: [0, 0, 0, 0, 0, 1, 1, 1, 0]
        [4, 5, 7] climb: [0, 0, 0, 0, 1, 1, 0, 1, 0]
        [6, 7, 8] .: [0, 0, 0, 0, 0, 0, 1, 1, 1]
    words:
    contexts:
    """

def test_train_mary():
    """
    >>> train = Train(Cells('Mary'))
    >>> train('','Mary')
    '<Mary>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
    """

def test_train_mary_likes_1():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans=train('','Mary')
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
    """

def test_train_mary_likes_2():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans=train('','Mary')
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train('<Mary>','likes')
    '<Mary likes>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (3, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
    """

def test_train_mary_likes_to():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans=train('','Mary')
    >>> ans = train('<Mary>','likes')
    >>> train('<Mary likes>','to')
    '<Mary likes to>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
    """

def test_train_mary_likes_to_sing():
    """
    >>> train = Train(Cells('Mary'))
    >>> train('Mary likes to sing .')
    '<Mary likes to sing .>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
        sing: ([4, 7, 8], '#1', [1 1 1; 0 0 0])
        .: ([6, 7, 8], '#1', [1 1 1; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
           sing: (1, '<Mary likes to sing>', [4, 7, 8])
        <Mary likes to sing>:
           #: ([4, 7, 8], '#1', 'sing')
           @: ['#1', [1 1 1; 0 0 0], '4.0-7.0-8.0']
           .: (1, '<Mary likes to sing .>', [6, 7, 8])
        <Mary likes to sing .>:
           #: ([6, 7, 8], '#1', '.')
           @: ['#1', [1 1 1; 0 0 0], '6.0-7.0-8.0']
    """

def test_train_mary_john():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans = train('Mary likes to sing .')
    >>> train('John')
    '<John>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#1', [1 1 1; 0 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
        sing: ([4, 7, 8], '#1', [1 1 1; 0 0 0])
        .: ([6, 7, 8], '#1', [1 1 1; 0 0 0])
        John: ([1, 7, 8], '#0', [0 0 0; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
           sing: (1, '<Mary likes to sing>', [4, 7, 8])
        <Mary likes to sing>:
           #: ([4, 7, 8], '#1', 'sing')
           @: ['#1', [1 1 1; 0 0 0], '4.0-7.0-8.0']
           .: (1, '<Mary likes to sing .>', [6, 7, 8])
        <Mary likes to sing .>:
           #: ([6, 7, 8], '#1', '.')
           @: ['#1', [1 1 1; 0 0 0], '6.0-7.0-8.0']
        <John>:
           #: ([1, 7, 8], '#0', 'John')
           @: ['#0', [0 0 0; 0 0 0], '1.0-7.0-8.0']
    """

def test_train_mary_john_likes():
    """
    >>> train = Train(Cells('Mary'))
    >>> ans = train('Mary likes to sing .')
    >>> train('John likes')
    '<John likes>'
    >>> train.show(token=False)
    words:
        Mary: ([0, 7, 8], '#0', [0 0 0; 0 0 0])
        likes: ([2, 7, 8], '#2', [0 1 1; 1 0 0])
        to: ([3, 7, 8], '#1', [1 1 1; 0 0 0])
        sing: ([4, 7, 8], '#1', [1 1 1; 0 0 0])
        .: ([6, 7, 8], '#1', [1 1 1; 0 0 0])
        John: ([1, 7, 8], '#0', [0 0 0; 0 0 0])
    contexts:
        <Mary>:
           #: ([0, 7, 8], '#0', 'Mary')
           @: ['#0', [0 0 0; 0 0 0], '0.0-7.0-8.0']
           likes: (1, '<Mary likes>', [2, 7, 8])
        <Mary likes>:
           #: ([2, 7, 8], '#1', 'likes')
           @: ['#1', [1 1 1; 0 0 0], '2.0-7.0-8.0']
           to: (1, '<Mary likes to>', [3, 7, 8])
        <Mary likes to>:
           #: ([3, 7, 8], '#1', 'to')
           @: ['#1', [1 1 1; 0 0 0], '3.0-7.0-8.0']
           sing: (1, '<Mary likes to sing>', [4, 7, 8])
        <Mary likes to sing>:
           #: ([4, 7, 8], '#1', 'sing')
           @: ['#1', [1 1 1; 0 0 0], '4.0-7.0-8.0']
           .: (1, '<Mary likes to sing .>', [6, 7, 8])
        <Mary likes to sing .>:
           #: ([6, 7, 8], '#1', '.')
           @: ['#1', [1 1 1; 0 0 0], '6.0-7.0-8.0']
        <John>:
           #: ([1, 7, 8], '#0', 'John')
           @: ['#0', [0 0 0; 0 0 0], '1.0-7.0-8.0']
           likes: (1, '<John likes>', [2, 7, 8])
        <John likes>:
           #: ([2, 7, 8], '#2', 'likes')
           @: ['#2', [0 1 1; 1 0 0], '2.1-7.0-8.0']
    """

def test_sequence():
    """
    >>> train = Train(Cells('Mary'))
    >>> train('Mary likes')
    '<Mary likes>'
    """

def test_andy1():
    """
    >>> train = Trainer(cells:=Cells((2,9,8,3),3))
    >>> train('Andy likes to climb')
    '<Andy likes to climb>'
    >>> cells.run('Andy',...)
    ['Andy', '->', 'likes', 'to', 'climb', '']
    """

def test_andy2():
    """
    >>> train = Trainer(cells:=Cells((2,9,8,3),3))
    >>> train('Andy likes to climb')
    '<Andy likes to climb>'
    >>> cells.run('Andy likes',...)
    ['Andy', 'likes', '->', 'to', 'climb', '']
    """

def test_andy3():
    """
    >>> train = Trainer(cells:=Cells((2,9,8,3),3))
    >>> train('Andy likes to climb')
    '<Andy likes to climb>'
    >>> cells.run('Andy likes',...)
    ['Andy', 'likes', '->', 'to', 'climb', '']
    """

def test_andy4():
    """
    >>> train = Trainer(cells:=Cells((2,9,8,3),3))
    >>> train('Andy likes to climb')
    '<Andy likes to climb>'
    >>> cells.run('Andy likes',...)
    ['Andy', 'likes', '->', 'to', 'climb', '']
    """

def test_mary_john_andy():
    """
    >>> train = Trainer(cells:=Cells((2,9,8,3),3))
    >>> train('Mary likes to sing')
    '<Mary likes to sing>'
    >>> train('John likes to dance')
    '<John likes to dance>'
    >>> train('Lisa likes to paint')
    '<Lisa likes to paint>'
    >>> train('Andy likes to climb')
    '<Andy likes to climb>'
    >>> cells.run('Mary',...)
    ['Mary', '->', 'likes', 'to', 'sing', '']
    >>> cells.run('John likes',...)
    ['John', 'likes', '->', 'to', 'dance', '']
    >>> cells.run('Lisa likes to',...)
    ['Lisa', 'likes', 'to', '->', 'paint', '']
    >>> cells.run('Andy likes to climb',...)
    ['Andy', 'likes', 'to', 'climb', '->', '']
    """

def test_lisa():
    """
    >>> train = Trainer(cells:=Cells((2,9,8,4),3))
    >>> train('Lisa likes to paint')
    '<Lisa likes to paint>'
    >>> cells.run('Lisa',...)
    ['Lisa', '->', 'likes', 'to', 'paint', '']
    """

#===============================================================================
# doc test
#===============================================================================

if __name__ == '__main__':
    import doctest
    doctest.testmod()
