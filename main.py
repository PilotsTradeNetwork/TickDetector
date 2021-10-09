# internal
from EDDNFuncs import EDDNThread
from IteratorFuncs import iteratorThread



def main():
    # 2 threads
    iteratorThread().start()
    print("IteratorThread started")
    EDDNThread().start()
    print("EDDNThread started")




if __name__ == '__main__':
    main()