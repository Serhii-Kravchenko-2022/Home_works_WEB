from time import time
from multiprocessing import Pool, cpu_count


def factorize(*number) -> dict:
    out_dict = {}
    for i in number:
        division_list = []
        count = 1
        while count <= i:
            if i % count == 0:
                division_list.append(count)
            count += 1
        out_dict[i] = division_list
    return out_dict


if __name__ == '__main__':
    processors = cpu_count()
    t1 = time()
    result = factorize(321, 1345, 9999, 106514460)
    print(f'час виконання лінійно: {time() - t1}')
    print(type(result), result)
    t2 = time()
    pool = Pool(processors)
    result = pool.apply_async(factorize, (321, 1345, 9999, 106514460))
    print(f'час виконання на {processors} процесорах {time() - t2}')
    print(type(result), result.get())
