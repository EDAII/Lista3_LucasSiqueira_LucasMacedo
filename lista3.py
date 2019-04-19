from time import time
from decimal import Decimal
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

TAM_LISTA = 100000
NUM_REPETICOES = 10 
INICIO_INTERVALO = 0
FIM_INTERVALO = 200000

def calc_media(results):
    averages = {}

    for key in results.keys():
        averages[key] = sum(results[key]) / len(results[key])
    return averages

def cria_lista_sem_repeticao():
    return random.sample(range(0, TAM_LISTA + 1), TAM_LISTA)

def cria_lista_com_repeticao():
    return [random.randint(INICIO_INTERVALO, FIM_INTERVALO) for x in range(TAM_LISTA)]

def plota_grafico(averages):
    plt.ylabel('Media de Tempo')

    for key in averages.keys():
        plt.bar(key, averages[key])

    plt.show()

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} wins)".format(pct, absolute)

def plota_grafico_pizza(wins):
    labels = wins.keys()
    valores = list(wins.values())
    ax = plt.subplots(figsize=(12, 9), subplot_kw=dict(aspect="equal"))[1]
    wedges, texts, autotexts = ax.pie(valores, autopct=lambda pct: func(pct, valores), textprops=dict(color="w"))
    ax.legend(wedges, labels, title="Algoritimos", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("Algoritimos de Busca")
    plt.show()

def partition(arr,low,high): 
    i = ( low-1 )         
    pivot = arr[high]     
  
    for j in range(low , high): 
        if   arr[j] <= pivot: 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
def quickSort(arr,low,high): 
    if low < high: 
        pi = partition(arr,low,high) 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 

def countingSort(arr, exp1): 
	n = len(arr) 
	output = [0] * (n) 
	count = [0] * (10) 

	for i in range(0, n): 
		index = (arr[i]//exp1) 
		count[ (index)%10 ] += 1

	for i in range(1,10): 
		count[i] += count[i-1] 

	i = n-1
	while i>=0: 
		index = (arr[i]//exp1) 
		output[ count[ (index)%10 ] - 1] = arr[i] 
		count[ (index)%10 ] -= 1
		i -= 1

	i = 0
	for i in range(0,len(arr)): 
		arr[i] = output[i] 

def radixSort(arr): 
	max1 = max(arr) 
	exp = 1

	while max1/exp > 0: 
		countingSort(arr,exp) 
		exp *= 10

def heapify(arr, n, i): 
	largest = i  
	l = 2 * i + 1	 
	r = 2 * i + 2	  

	if l < n and arr[i] < arr[l]: 
		largest = l 

	if r < n and arr[largest] < arr[r]: 
		largest = r 

	if largest != i: 
		arr[i],arr[largest] = arr[largest],arr[i] 

		heapify(arr, n, largest) 

def heapSort(arr): 
	n = len(arr) 

	for i in range(n, -1, -1): 
		heapify(arr, n, i) 

	for i in range(n-1, 0, -1): 
		arr[i], arr[0] = arr[0], arr[i] 
		heapify(arr, i, 0)

def mergeSort(arr): 
    if len(arr) >1: 
        mid = len(arr)//2  
        L = arr[:mid]   
        R = arr[mid:] 
  
        mergeSort(L) 
        mergeSort(R) 
  
        i = j = k = 0
          
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1 

if __name__ == "__main__":
    results = {'Quick': [], 'Heap': [], 'Radix': [], 'Merge': []}
    result = {'Quick': 0, 'Heap': 0, 'Radix': 0, 'Merge': 0}
    wins = {'Quick': 0, 'Heap': 0, 'Radix': 0, 'Merge': 0}
    verifica_empate = set()
    qtd_empates = 0

    for aux in range(NUM_REPETICOES):
        lista = cria_lista_sem_repeticao()
        lista_com_repeticao = cria_lista_com_repeticao()

        for key in result.keys():
            if key == 'Quick':
                inicio = time()
                # quickSort(lista.copy())
                quickSort(lista_com_repeticao.copy(), 0, len(lista_com_repeticao) - 1)
            elif key == 'Heap':
                inicio = time()
                # heapSort(lista.copy())
                heapSort(lista_com_repeticao.copy())
            elif key == 'Merge':
                inicio = time()
                # mergeSort(lista.copy())
                mergeSort(lista_com_repeticao.copy())
            else: 
                inicio = time()
                # radixSort(lista.copy())
                radixSort(lista_com_repeticao.copy())
    
            fim = time()
            tempo = Decimal(fim - inicio)

            result[key] = tempo
            results[key].append(tempo)

            verifica_empate.add(tempo)

        if len(verifica_empate) != 3:
            qtd_empates += 1

        verifica_empate = set()
         
        lis = list(result.items())
        winner = min(lis,key=lambda item:item[1])

        wins[winner[0]] += 1



    print('Quantidade de empates: ', qtd_empates)

    averages = calc_media(results)

    print('\n\t \t \tResultado em Wins:')
    for key in wins.keys():
        print(key + ': ' + str(wins[key]))

    print('\n\t \t \tMedia de Tempo:')
    for key in averages.keys():
        print(key + ': ' + str(averages[key]))
    
    plota_grafico_pizza(wins)
    plota_grafico(averages)