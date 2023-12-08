def image_to_real(list_E,list_f2):
    
    def g(x,y):
        if x==y:
            return (x+y)*math.log(x+y)
        elif y == math.inf:
            return 0
        else:
            return (x+y)*math.log(x+y)+(x-y)*math.log(abs(x-y))

    def kk_linearfit(w,w0,w1,w2):
        return (g(w0,w)/(w1-w0)-(w2-w0)*g(w1,w)/(w1-w0)/(w2-w1)+g(w2,w)/(w2-w1))

    # 초반 외삽 (x^2으로 피팅)
    def kk_expol_front(w,w1,w2):
        def f(w,w1,w2):
            if -1*w == w1:
                return 0
            else:
                return (w**2/w1**2-(w2+w)/(w2-w1))*math.log(abs(w1+w))
        return (-1-2*w**2/w1**2*math.log(w)+g(w2,w)/(w2-w1)+f(w,w1,w2)+f(-1*w,w1,w2))
    
    # 후반 외삽 (x^-1으로 피팅) 
    def kk_expol_end1(w,w0,w1):
        def f(w,w0,w1):
            if -1*w == w1:
                return 0
            else:
                return (w1/w-(w0+w)/(w1-w0))*math.log(abs(w1+w))
        return (2+g(w0,w)/(w1-w0)+f(w,w0,w1)+f(-1*w,w0,w1))
    
    list_newf1 = []
    for i in range(len(list_E)):
        w_n=list_E[i]
        kk_sum = 0
        for j in range(len(list_E)):
            if j==0:
                x1 = list_E[0]; x2 = list_E[1]; y = list_f2[0]
                kk_sum += y * kk_expol_front(w_n,x1,x2)
            elif j==len(list_E) - 1:
                x0 = list_E[j-1]; x1 = list_E[j]; y = list_f2[j]
                kk_sum += y * kk_expol_end1(w_n,x0,x1)
            else:
                x0 = list_E[j-1]; x1 = list_E[j]; x2 =list_E[j+1]; y = list_f2[j]
                kk_sum += y * kk_linearfit(w_n,x0,x1,x2)
        list_newf1.append(kk_sum/math.pi)
    
    return list_newf1


def real_to_image(list_E,list_f1,x0=1):
    
    def g(x,y):
        if x==y:
            return (x+y)*math.log(x+y)
        elif y == math.inf:
            return 0
        else:
            return (x+y)*math.log(x+y)+(x-y)*math.log(abs(x-y))
    
    def kk_linearfit(w,w0,w1,w2):
        return g(w,w0)/(w0-w1)+(w2-w0)*g(w,w1)/(w1-w0)/(w2-w1)+g(w,w2)/(w1-w2)

    list_newf1 = []
    for i in range(len(list_E)):
        w_n=list_E[i]
        kk_sum = 0
        for j in range(len(list_E)):
            if j==0:
                x1 = list_E[0]; x2 = list_E[1]; y = list_f1[0]
                kk_sum += y * kk_expol_front(w_n,x1,x2)
            elif j==len(list_E) - 1:
                x0 = list_E[j-1]; x1 = list_E[j]; y = list_f1[j]
                kk_sum += y * kk_expol_end1(w_n,x0,x1)
            else:
                x0 = list_E[j-1]; x1 = list_E[j]; x2 =list_E[j+1]; y = list_f1[j]
                kk_sum += y * kk_linearfit(w_n,x0,x1,x2)
        list_newf1.append(kk_sum/math.pi)

    return list_newf1