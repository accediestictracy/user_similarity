users_matrix = []

for i in users:
    users_matrix.append([])
    for j in users:
        clist = common(i, j)     #common labels of user i and user j
        num = len(clist)
        for k in clist:
            i_child.append(child(k,i))# topics of user_i in group[k]
            j_child.append(child(k,j))# topics of user_j in group[k]

            for tag in (i_child):
                vec_i += word2vec(itag) * senti_score(i_child)
            for tag in (j_child):
                vec_j += word2vec(itag) * senti_score(j_child)

        users_matrix[-1].append(cos(vec_i, vec_j)*num)

