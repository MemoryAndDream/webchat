#coding=utf8
import importlib
if __name__=='__main__':
    print 'test'
    #mo =importlib.import_module('.'.join(["crawler",'extractors','universal']))
    mo =importlib.import_module('.'.join(["crawler",'extractors','360kan']))

    print mo.process("暴走恐怖故事 第五季",'1')
