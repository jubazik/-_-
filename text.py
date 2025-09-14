n = {6, 2, 1, 8, 10 }
print(len(n))
def sum_array(arr):
    if len(arr)> 1 or arr  not  in {'null', None, 'Nothing', 'nil', 'etc'}:
        arr.remove(max(arr))
        arr.remove(min(arr))
        return sum(arr)
    else:
        return 0
print(sum_array(n))



# n.remove()
print(n)