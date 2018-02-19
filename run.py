# Implementation of MS-APRIORI
# Authors : Vanisre Jaiswal,Charvi Virani


# Import Libraries
import operator

# main function
def main():
    # Read input and MIS values from files
    read_mis("/Users/vanijais/PycharmProjects/project_dmtm/MIS.txt")
    read_data("/Users/vanijais/PycharmProjects/project_dmtm/input.txt")

    # Initializing constants
    sort = []
    L = []
    candid2 = []
    candidate_set = []
    frequent_set = []
    must_have = constraint[1]
    not_together = constraint[0]
    n = len(input_data)
    
    # MIS_algorithm
    sort = sort_mis_values(input_data, para_data)
    L = init_pass(sort, input_data)
    candid2 = gen_candidate2(L, para_data['SDC'])
    frequent_set.append(L)  
    frequent_set.append(First_freq(L, must_have))  
    for i in range(2, 100, 1):
        if not frequent_set[i - 1]:
            del frequent_set[-1]
            if len(candidate_set) >= 1:
                del candidate_set[-1]
            break
        else:  
            if i <= 2:  
                candid2 = gen_candidate2(frequent_set[0], para_data['SDC'])
                candidate_set.append(candid2)
            else:
                
                candidate_set.append(MSCandidateGeneration(frequent_set[i - 1], para_data['SDC']))

            frequent_set.append(NextFrequent(candidate_set[i - 2], para_data, input_data, must_have,
                              not_together))  

    output(frequent_set, input_data)  


# Read input and store in input_data
input_data = []
def read_data(data_file):
    with open(data_file) as f:
        for line in f:
            l = list(line)
            p1 = l.index("{")
            p2 = l.index("}")
            line = line[p1 + 1:p2]
            l00 = line.split(", ")  
            input_data.append(l00)



#Read MIS values and store in Para_data
constraint = []
para_data = {}
def read_mis(mis_file):
    with open(mis_file) as f:
        for line in f:
            line = line.rstrip()
            if "=" in line:
                key, value = line.split(" = ")
                if key[0:3] == 'MIS':
                    key = key[4:-1]
                para_data[key] = float(value)
            if ":" in line:
                a, b = line.split(": ")
                if a == 'cannot_be_together':
                    p1 = b.index("{")
                    p2 = b.index("}")
                    b = b[p1 + 1:p2]
                    b = b.split(", ")

                    constraint.append(b[:])

                if a == 'must-have':
                    b = b[:]
                    b = b.split(" or ")
                    constraint.append(b[:])


# check item in given set
def check_item(item, set):
    if item in set:
        return True
    else:
        return False


# check the support count
def support_count(item, data):
    n = 0
    for i in data:
        if check_item(item, i):
            n = n + 1
    return n


# sort items in data according to MIS value.
def sort_mis_values(data, mis):
    temp_seq = {}
    for i in mis.keys():
        for j in data:
            if i in j:
                temp_seq[i] = mis[i]
    sort_mis_values = sorted(temp_seq.items(), key=operator.itemgetter(1))
    return sort_mis_values


# First scan the data 
def init_pass(sort, data):
    n = len(data)
    L = []
    for i in sort:  
        if support_count(i[0], data) >= (n * para_data[i[0]]):
            L.append(i[0])
            p = sort.index(i)
            l_sort = sort[p + 1:len(sort)]
            for j in l_sort:
                if support_count(j[0], data) >= (n * para_data[L[0]]):
                    L.append(j[0])
            return L


# level2 candidate generation 
def gen_candidate2(L, SDC):
    n = len(input_data)
    candid2 = []
    for l in L:
        if support_count(l, input_data) >= (para_data[l] * n):
            L0 = []
            p = L.index(l)
            L0 = L[p + 1:len(L)]
            for h in L0:
                if support_count(h, input_data) >= (para_data[l] * n) and abs(
                        support_count(h, input_data) - support_count(l, input_data)) <= (n * SDC):
                    c = []
                    c = [l, h]
                    candid2.append(c)
    return candid2


# Frequent itemset_1_1s F1 are obtained from L.
def First_freq(L, cnst):
    F1 = []
    n = len(input_data)
    for l in L:
        if support_count(l, input_data) >= (para_data[l] * n):
            if l in cnst:
                F1.append([l])
    return F1


# find subsets .
def subsets(itemset_1):
    subset = []
    for i in itemset_1:
        j = []
        p = itemset_1.index(i)
        j = itemset_1[:p] + itemset_1[p + 1:]
        subset.append(j)
    return subset


# MScandidate generation function for other level
def MSCandidateGeneration(F, SDC):
    C = []
    n = len(input_data)

    # join step
    for i in F:
        for j in F:
            if i[0:-1] == j[0:-1] and i[-1] < j[-1] and abs(
                    support_count(i[-1], input_data) - support_count(j[-1], input_data)) <= (n * SDC):
                c = []
                c = i[:]

                c.append(j[-1])
                C.append(c)
    # prune step
    for k in C:
        p = C.index(k)
        subset = []
        subset = subsets(k)
        for j in subset:
            if k[0] in j or para_data[k[0]] == para_data[k[1]]:
                if j not in F:
                    del C[p]
                    break

    return C


# Generated frequent itemset
def NextFrequent(C_k, mis, data, must_have, not_together):
    NextFrequent = []
    n = len(data)
    for c in C_k:
        if musthave_exists(must_have, c):
            if not together_exists(c, not_together):

                if supp_of_seq(c, data) >= n * para_data[c[0]]:
                    NextFrequent.append(c)

    return NextFrequent


#  record the support count of given data
def supp_of_seq(seq, data):
    n = 0
    for i in data:
        for j in seq:
            if j not in i:
                break
        else:
            n = n + 1
    return n


# check if any must-have item exists in given dataset/itemset
def musthave_exists(must_have, itemset_1):
    for i in must_have:
        if i in itemset_1:
            return True
    return False


# check if any not-together item exists in given dataset/itemset
def together_exists(itemset_1, not_together):
    n = 0
    for i in not_together:
        if i in itemset_1:
            n = n + 1
        if n == 2:
            return True

    return False


# Gives output
def output(freq_items, data):
    freq_items = freq_items[1:]
    for i in freq_items:
        n = freq_items.index(i) + 1
        print('Frequent %d-itemset_1s \n' % n)

        for j in i:
            j_output = '{' + str(j).strip('[]') + '}'
            print('\t%d : %s' % (supp_of_seq(j, data), j_output))
            # Tailcount
            if len(j) > 1:
                j_tail = j[1:]
                j_tailcount = supp_of_seq(j_tail, data)
                print('Tailcount = %d' % j_tailcount)
        print('\n\tTotal number of frequent %d-itemset_1s = %d\n\n' % (n, len(i)))


if __name__ == "__main__": main()