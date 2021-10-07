# internal
from EDDNFuncs import EDDNThread
from IteratorFuncs import iteratorThread



def main():
    # 2 threads
    iteratorThread().start()
    EDDNThread().start()




if __name__ == '__main__':
    main()