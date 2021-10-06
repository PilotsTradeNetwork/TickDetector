# external
from system import System

# internal
from EDDNFuncs import EDDNThread
from IteratorFuncs import iteratorThread

global systemList
systemList = [System]

def main():
    # 2 threads
    iteratorThread().start()
    EDDNThread().start()




if __name__ == '__main__':
    main()