from EDDNFuncs import EDDNThread
from IteratorFuncs import IteratorThread

def main():
    IteratorThread().start()
    EDDNThread().start()

if __name__ == '__main__':
    main()