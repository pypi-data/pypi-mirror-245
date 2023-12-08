def image_to_real(list_E,list_f2):

    def kk_linearfit(w,w0,w1,w2):
        if w == w0:
            return (w2-w)/(w2-w1)*math.log(abs((w2-w)/(w1-w)))+(w2-w0)
        if w == w2:
            return (w-w0)/(w1-w0)*math.log(abs((w1-w)/(w0-w)))+(w2-w0)
        if w == w1:
            return -math.log(abs(w0-w))+math.log(abs(2-w))+(w2-w0)
        else:
            return (w-w0)/(w1-w0)*math.log(abs((w1-w)/(w0-w)))+(w2-w)/(w2-w1)*math.log(abs((w2-w)/(w1-w)))+(w2-w0)
    
    def kk_expol(w,w1,w0)
        return 


    list_newf1 = []
    for i in range(len(list_E)):
        w_n=list_E[i]
        kk_sum = 0
        for j in range(len(list_E)):
            if j==0:
                x1 = list_E[0]; x2 = list_E[1]; y = list_f2[0]
                kk_sum += y * -1 * kk_expol(w_n,x1,x2)
            elif j==len(list_E) - 1:
                x0 = list_E[j-1]; x1 = list_E[j]; y = list_f2[j]
                kk_sum += y * kk_expol(w_n,x1,x0)
            else:
                x0 = list_E[j-1]; x1 = list_E[j]; x2 =list_E[j+1]; y = list_f2[j]
                kk_sum += y * kk_linearfit(w_n,x0,x1,x2)
        list_newf1.append(kk_sum/math.pi)
    
    return list_newf1    


def image_to_real(list_E,list_f2):

    def kk_linearfit(w,w0,w1,w2):
        if w == w0:
            return (w2-w)/(w2-w1)*math.log(abs((w2-w)/(w1-w)))+(w2-w0)
        if w == w2:
            return (w-w0)/(w1-w0)*math.log(abs((w1-w)/(w0-w)))+(w2-w0)
        if w == w1:
            return -math.log(abs(w0-w))+math.log(abs(2-w))+(w2-w0)
        else:
            return (w-w0)/(w1-w0)*math.log(abs((w1-w)/(w0-w)))+(w2-w)/(w2-w1)*math.log(abs((w2-w)/(w1-w)))+(w2-w0)
    
    def kk_expol(w,w1,w0)
        return 


    list_newf1 = []
    for i in range(len(list_E)):
        w_n=list_E[i]
        kk_sum = 0
        for j in range(len(list_E)):
            if j==0:
                x1 = list_E[0]; x2 = list_E[1]; y = list_f2[0]
                kk_sum += y * -1 * kk_expol(w_n,x1,x2)
            elif j==len(list_E) - 1:
                x0 = list_E[j-1]; x1 = list_E[j]; y = list_f2[j]
                kk_sum += y * kk_expol(w_n,x1,x0)
            else:
                x0 = list_E[j-1]; x1 = list_E[j]; x2 =list_E[j+1]; y = list_f2[j]
                kk_sum += y * kk_linearfit(w_n,x0,x1,x2)
        list_newf1.append(kk_sum/math.pi*-1)
    
    return list_newf1  