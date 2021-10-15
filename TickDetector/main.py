from EDDNThread import EDDNThread
from IteratorThread import IteratorThread

def main():
    IteratorThread().start()
    EDDNThread().start()

if __name__ == '__main__':
    main()