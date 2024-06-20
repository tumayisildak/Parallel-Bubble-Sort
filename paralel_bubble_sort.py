import time
import random
import threading
import itertools

# Çalışma süresini hesaplamak için zaman sayacını başlat
start_time = time.time()

# Thread kilidi oluştur
lock = threading.Lock()

# bubble sort fonksiyonu
def bubblesort(lst):
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
# Bu fonksiyon normal bubble sort fonksiyonunu kullanır
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
    print(final_lst)

# Test etmek için 1000 elemanlı bir örnek liste
lst = [random.randint(0, 1000000) for i in range(1000)]
Parallel_bubble_sort(lst)

end_time = time.time() - start_time
print("--- %s saniye sürdü ---" % (end_time))
