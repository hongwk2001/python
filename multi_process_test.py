import multiprocessing as mp

def f(x):
    return x*x

if __name__ == '__main__':
    with mp.Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
        