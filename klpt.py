import random

print("请输入机器的数量,以回车结束")
machine_num = int(input())

basic_price = []
time_price = []

print("随机产生每个机器的基本费用[1, 10]、单位价格费用[1, 5]")
for i in range(machine_num):
    basic_price.append(random.randint(1,10))
    time_price.append(random.randint(1,5))
print("basic_price: ", basic_price)
print("time_price: ", time_price)

print("请输入job的数量,以回车结束")
job_num = int(input())
processing_time = []
print("随机产生每个job的processing time")
for i in range(job_num):
    processing_time.append(random.randint(1,20))
ls_processing_time = processing_time.copy()
processing_time.sort()
processing_time.reverse()
print("processing_time: ", processing_time)
print("")

######################## 参数计算: buget_cost ##########################
ramta = 0.6
P = sum(processing_time)
Pmax = max(processing_time)
c_star = []
# LPT算法在计算k个machine之前要先将Pj排序
for i in range(machine_num):
    c_star.append( max( [P/(i+1), Pmax] ) )

u_upper_bound = 0 # 上界
u_upper_bound += sum(basic_price)
for i in range(machine_num):
    u_upper_bound += time_price[i] * c_star[machine_num-1]

u_lower_bound_tmp = []
for i in range(machine_num):
    u_lower_bound_tmp.append(time_price[i] * c_star[0] + basic_price[i])
# print("u_lower_bound_tmp: ", u_lower_bound_tmp)
u_lower_bound = min(u_lower_bound_tmp) # 下界

buget_cost = u_lower_bound + ramta * (u_upper_bound - u_lower_bound)
print("u_upper_bound: ", u_upper_bound)
print("u_lower_bound: ", u_lower_bound)
print("buget_cost: ", buget_cost)
print("")
######################## 参数计算: k ################################

k = 0
for i in range(machine_num):
    # 每次循环 计算一遍 ai * (Ci*) + bi, 放进数组cost_tmp[]中 
    cost_tmp = []
    for iii in range(machine_num):
        cost_tmp.append(time_price[iii] * c_star[i] + basic_price[iii])
    ttt = {} # 这个字典key是原来机器排序的序号 value是每个机器的费用
    for iii in range(machine_num):
        ttt[str(iii+1)] = cost_tmp[iii] # 原来机器随机排序的每个机器的费用
    ttt_list = sorted(ttt.items(),key=lambda item:item[1]) # 按照value大小排序,从小到大
    cost_res = 0 # 最终的cost: Ci*是前i个机器的费用之和
    for iii in range(i+1):
        cost_res += ttt_list[iii][1]
    print("cost_res: ", cost_res)
    if i == machine_num-1:
        k = machine_num
        break
    else:
        if cost_res > buget_cost: # 如何中间的第i台机器费用超了, k就取i 
            k = i+1 # 循环下标是从0开始,所以要 +1
            break
print("最佳使用 " + str(k) , " 台机器, 分别是:")
for i in range(k):
    print("使用了第 " + ttt_list[i][0] + "台机器")
print("")

##################### 参数计算 fc * R ##############################

# 现在的这k台机器也是有顺序的，平均花费Ck* 从小到大，前面计算过了
k_machine_basic_price = [] # 重新创建价格数组,之后的计算以这为准
k_machine_time_price = []
for i in range(k):
    k_machine_basic_price.append(basic_price[int(ttt_list[i][0])-1])
    k_machine_time_price.append(time_price[int(ttt_list[i][0])-1])
print("排序后的机器基础费用：", k_machine_basic_price)
print("排序后的机器单位费用：", k_machine_time_price)


epsilon = 0.01
fc = 0
R = 0
c_k_star = c_star[k-1]
c_k_1_star = c_star[k-2]
# 二分查找
right = c_k_1_star
left = c_k_star
gap = right - left
#print("gap0: ", gap)
while gap > epsilon:
    #print("gap: ", gap)
    mid = left + (right - left)/2
    ccost = 0
    for i in range(k-1):
        ccost += k_machine_time_price[i]*mid + k_machine_basic_price[i]
    ccost += (k_machine_time_price[k-1]*(k*c_k_star-(k-1)*mid))+k_machine_basic_price[k-1]
    
    if ccost > buget_cost:
        # right 不变
        left = mid
    else:
        # left 不变
        right = mid

    gap = right - left
        
fc = left
R = k*c_k_star - (k-1)*left
print("fc: ", fc)
print("R: ", R)
print("")        

################### LPT的改进算法 #########################

# 已知参数 k_machine_basic_price、k_machine_time_price、R
k_1_machine_load = [] 
kth_machine_load = 0 # 最后那台机器单独算
for i in range(k-1):
    k_1_machine_load.append(0)


for i in range(job_num):
    if processing_time[i] <= (R - kth_machine_load):
        kth_machine_load += processing_time[i]
        #print("job "+str(i+1)+" 在最后那台machine k上处理")
        #print("处理job"+str(i+1)+"后, machine k的加工时间为: "+str(kth_machine_load)+" R = "+str(R))
    else:
        iindex = k_1_machine_load.index(min(k_1_machine_load))
        k_1_machine_load[iindex] += processing_time[i]
        #print("job "+str(i+1)+" 在machine "+str(iindex+1)+" 上处理")
        #print("处理job "+str(i+1)+"之后前k-1台机器加工时间分别为: ", k_1_machine_load)

print("上面已经将所有job预处理完了，下面要再重新排序，工件长的放到价格便宜的机器上")
k_machine_load = []
for i in range(k-1):
    k_machine_load.append(k_1_machine_load[i])
k_machine_load.append(kth_machine_load)
k_machine_load.sort()
k_machine_load.reverse()
print("最终k台机器的加工时间分别为: ", k_machine_load)
print("")
total_cost = 0
total_cost += sum(k_machine_basic_price)
for i in range(k):
    total_cost += k_machine_time_price[i] * k_machine_load[i]
print("total_cost: ", total_cost)

print("########################## 下面进行LS ############################")
print("########################## 下面进行LS ############################")
kk_machine_time = [] # 机器数 k-1 减去最后那台机器
print("ls_processing_time: ", ls_processing_time)
for i in range(k-1):
    kk_machine_time.append(0)
for i in range(job_num):
    iindex = kk_machine_time.index(min(kk_machine_time))
    kk_machine_time[iindex] += ls_processing_time[i]
    #print("job "+str(i+1)+" 在machine "+str(iindex+1)+" 上处理")
    #print("处理job "+str(i+1)+"之后每台机器加工时间为: ", kk_machine_time)

kk_machine_time.sort()
kk_machine_time.reverse()
print("将machine的load预处理, 由大到小排序,在分别放到便宜的机器上")
print("kk_machine_time: ", kk_machine_time)

print("Cmax = ", max(kk_machine_time))
total_cost = 0
k_machine_basic_price.pop()
k_machine_time_price.pop()
total_cost += sum(k_machine_basic_price)
for i in range(k-1):
    total_cost += k_machine_time_price[i] * kk_machine_time[i]
print("total_cost = ", total_cost)














