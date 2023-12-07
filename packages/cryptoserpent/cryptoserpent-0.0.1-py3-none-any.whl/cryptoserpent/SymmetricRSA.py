import numpy as _np
from time import perf_counter as _perf_counter
import random as _random
from hashlib import sha256 as _sha256
import warnings as _warnings 

class SymmetricRSA:
    def __init__(self, n_dims:int, seed:str=None):
        if seed is not None and len(seed) < 8:
            print('Random Seed should be at least 8 characters for security.')
        if n_dims < 3:
            print('n_dims should be at least 3 (preferably 5) for seurity')
        elif n_dims < 24:
            raise ValueError('n_dims greater than 24 not supported')
        self.n_dims = n_dims
        self.primes = None

        self.seed = self.__gen_seed() if (seed is None) else seed
        self.__seed = int.from_bytes(_sha256(self.seed.encode()).digest())
        _random.seed(self.__seed)
        
        if self.primes is None:
            self.primes = _np.load("../data/10-digit-primes.npy")
        
        self.__keys = self.__gen_keys()
        self.__inv_keys = [_np.linalg.inv(i) for i in self.__keys]

        self.__key_mappings = {arr[0][0]:i for i, arr in enumerate(self.__keys)}
        self.__inv_key_mappings = {arr[0][0]:i for i, arr in enumerate(self.__inv_keys)}

        _warnings.filterwarnings('ignore')

        # do this to save space
        del self.primes

    def encrypt(self, text:str) -> _np.ndarray:
        if len(text)%2 != 0:
            text += ' '
        
        res = []
        for i in range (0, len(text), 2):
            res.append(
                self.__keys[ord(text[i])] @ self.__keys[ord(text[i+1])]
            )
        res = _np.array(res, dtype=_np.float64)
        res = _np.stack(res).reshape((-1))
        return self.__add_random_end(res)

    def decrypt(self, code:_np.ndarray) -> str:
        if code.shape[0] % (self.n_dims**2) != 0:
            code = code[:-1*(code.shape[0]%(self.n_dims**2))]
        
        code = code.reshape(-1, self.n_dims, self.n_dims)
        res = ''
        for arr in code:
            for inv in self.__inv_keys:
                r = _np.matmul(inv, arr).round().astype(int)
                if self.__key_mappings.get(r[0][0]) is not None:
                    res += chr(self.__inv_key_mappings[inv[0][0]]) + chr(self.__key_mappings[r[0][0]])
        return res

    def __add_random_end(self, arr:_np.ndarray):
        num_add = _random.randint(0, self.n_dims**2-1)
        suffix = _np.array([_random.choice(arr) for _ in range (num_add)], dtype=_np.float64)
        return _np.concatenate([arr, suffix])

    def __gen_keys(self) -> list:
        res = []
        current_starts:set = {0}
        for _ in range (256):
            ph = _np.zeros((self.n_dims, self.n_dims))
            while (ph[0][0] in current_starts):
                for i in range(self.n_dims):
                    for j in range (self.n_dims):
                        ph[i][j] = _random.choice(self.primes)
            current_starts.add(ph[0][0])
            res.append(ph)
        return res

    def __gen_seed(self) -> str:
        start = _perf_counter()
        self.primes = _np.load("../data/10-digit-primes.npy")
        end = _perf_counter()
        # Use time taked for IO oprtation as an additional source of entropy
        return _sha256(f'{start}{end}{_random.random()}'.encode()).hexdigest()
