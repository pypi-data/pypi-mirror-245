# -*- coding:utf-8 -*-  
from os import path,listdir,unlink,makedirs
from collections.abc import Iterator
import shutil
class DIRBase(object):
    def __init__(self,abs_path):
        assert path.isabs(abs_path) , ValueError("请输入绝对路径")
        self.__path = abs_path
    
    @property
    def str(self):
        return self.__path
    
    def __str__(self):
        return self.str
    
    def __sub__(self,other):
        return path.relpath(str(other),str(self))
    
    def __repr__(self):
        return "<{classname} {p}>".format(classname=self.__class__.__name__,p=self.str)
    
class DFile(DIRBase):
    def __init__(self, abs_path,fname):
        super().__init__(abs_path)
        
        self.__fname,self.__fext = path.splitext(fname)
    
    @property
    def fname(self):
        return self.__fname
    @property
    def fext(self):
        return self.__fext if self.__fext else None
    @property
    def full_fname(self):
        return "".join([self.__fname,self.__fext])
    @property
    def str(self):
        return path.join(super().str,self.full_fname)
    
    def __bool__(self):
        return path.isfile(self.str)
    @property
    def parent(self):
        return DRoot(super().str)
    @property
    def open(self):
        if not self.parent:
            self.parent.makedirs()
        def _p(*args,**kw):
            return open(str(self),*args,**kw)
        return _p
    def __lshift__(self,value):
        if not self.parent:
            self.parent.makedirs()
        with open(self.str,'w') as fp:
            fp.write(value)
        return self
    def __ilshift__(self,value):
        if not self.parent:
            self.parent.makedirs()
        with open(self.str,"a") as fp:
            fp.write(value)
        return self
    def __rlshift__(self,other):
        if not self.parent:
            self.parent.makedirs()
        with open(self.str,"r") as fp:
            other = fp.read()
        return other
    
    def unlink(self):
        unlink(str(self))
        return self
    def cp(self,dist_fpath:str):
        shutil.copyfile(str(self), str(dist_fpath) )
        return  self.__class__(*path.split(str(dist_fpath)))
    def mv(self,dist_fpath:str):
        resp = self.cp(dist_fpath)
        self.unlink()
        return resp
        
class _droot_iter(Iterator):
    def __init__(self,dObject):
        super().__init__()
        self.__obj = dObject
        self.__data = listdir(str(dObject))
        self._i = 0
    def __iter__(self) :
        return self
    def __next__(self):
        if self._i < len(self.__data):
            i = self._i
            self._i+=1
            name = self.__data[i]
            p = path.join(self.__obj.str,name)
            if path.isfile(p):
                return self.__obj.as_file(name)
            else:
                return self.__obj[name]
        else:
            raise StopIteration
    
        
class DRoot(DIRBase):
    def __init__(self, abs_path):
        super().__init__(abs_path)
        
    def __getitem__(self,k):
        return self.__class__(path.join(self.str,k))
    
    def __bool__(self):
        return path.isdir(self.str)
    def __iter__(self):
        return _droot_iter(self)
    def __call__(self, fname):
        return self.as_file(fname)
    def as_file(self,fname):
        return DFile(str(self),fname)
    def makedirs(self):
        if path.isdir(str(self)):
            return self
        makedirs(str(self))
        return self
    def makeAndClear(self):
        if path.isdir(str(self)):
            shutil.rmtree(str(self))
        return self.makedirs()
    @classmethod
    def from_file(cls,fpath):
        fpath = path.dirname(fpath)
        p =fpath if path.isabs(fpath) else path.abspath(fpath)
        return cls(p)
    @property
    def parent(self):
        return DRoot(path.dirname(self.str))
    
    def tree(self,deep=0,ident=4):
        ret = []
        for item in self:
            
            if isinstance(item,DFile):
                if item.fname[0]=='.':
                    continue
                ret.append( ' '*ident*deep + item.full_fname)
            if isinstance(item,DRoot):
                ret = [ *ret , ' '*ident*deep + path.split(item.str)[-1] ,*item.tree(deep+1,ident)]
        return ret
        
            


        


            

