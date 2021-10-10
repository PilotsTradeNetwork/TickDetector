# internal
from EDDNFuncs import EDDNThread
from IteratorFuncs import iteratorThread



def main():
    # # 2 threads
    # a = ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'b']
    # a.append('c')
    # a.pop(0)
    # # a[:] = [x for x in a if x == 'a']
    # print(a)
    # input()


    iteratorThread().start()
    print("IteratorThread started")
    EDDNThread().start()
    print("EDDNThread started")




if __name__ == '__main__':
    main()