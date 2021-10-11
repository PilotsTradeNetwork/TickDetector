from EDDNFuncs import EDDNThread
from IteratorFuncs import iteratorThread

def main():
    iteratorThread().start()
    EDDNThread().start()

if __name__ == '__main__':
    main()