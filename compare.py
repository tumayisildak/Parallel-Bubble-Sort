import time
import threading
import itertools
import random

def measure_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time

# Ortak liste
lst = [random.randint(0, 10000) for i in range(10000)]

def bubble_sort_3(lst):
    # Doğru sıralayan paralel3.py içeriği
    def bubblesort(lst):
        lock = threading.Lock()
        # Thread için kilidi üret
        lock.acquire()
        
         # Listenin uzunluğunu al
        n = len(lst)
        
        # Bubble sort işlemi gerçekleştir
        for i in range(n):
            swap = False
            for j in range(0, n-i-1):
                if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    swap = True
            if not swap:
                break
        
        # Hesaplamadan sonra kilidi serbest bırak
        lock.release()

    # Paralel bubble sort fonksiyonu oluştur
    def Parallel_bubble_sort(lst): 
        # Listedeki en büyük elemanı al
        biggest_item = max(lst)
        
        # Çekirdek sayısına göre thread sayısını ayarla
        no_threads = 16
        
        # Thread sayısına göre alt listeler oluştur
        lists = [[] for _ in range(no_threads)]
        
        # Listeyi her alt liste için sınıf aralıklarına bölmek için bir sayı kullanıyoruz
        split_factor = biggest_item // no_threads

        # Thread sayısına göre listeyi alt listelere böl
        for j in range(1, len(lists)):
            for i in lst:
                if i <= (split_factor * j):
                    lists[j-1].append(i)
                    # Elemanı alt listeye ekledikten sonra listeden çıkar
                    # Çoğaltmayı önlemek için
                    lst = [x for x in lst if x != i]
            # Kalan elemanları son alt listeye dahil et
            lists[-1] = lst

        # Her alt liste için tüm thread'leri başlat
        active_threads = []
        for list_item in lists:
            t = threading.Thread(target=bubblesort, args=(list_item,))
            t.start()
            active_threads.append(t)
            
        # Tüm aktif thread'leri durdur
        for thread in active_threads:
            thread.join()

        # Tüm listeleri son listeye birleştir
        final_lst = list(itertools.chain(*lists))
        
        
    # Sıralı listeyi yazdır
    Parallel_bubble_sort(lst)

def bubble_sort_normal(lst):
    # Normal bubble sort
    for n in range(len(lst)-1, 0, -1):
        swapped = False
        for i in range(n):
            if lst[i] > lst[i + 1]:
                swapped = True
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
        if not swapped:
            return

def main():
    # Paralel Bubble Sort Algoritmalarını ve normal bubble sort algoritmasını çalıştır ve sürelerini ölç
    time_normal = measure_time(bubble_sort_normal, lst.copy())
    time3 = measure_time(bubble_sort_3, lst.copy())

    # Sonuçları yazdır
    print(f"paralel Bubble Sort çalışma süresi: {time3:.6f} saniye")
    print(f"Normal Bubble Sort çalışma süresi: {time_normal:.6f} saniye")
if __name__ == "__main__":
    main()
