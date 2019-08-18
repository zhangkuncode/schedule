import random

print("请输入机器的数量,以回车结束")
machine_num = int(input())

basic_price = []
time_price = []
machine_time = []
print("随机产生每个机器的基本费用[1, 10]、单位价格费用[1, 5]")
for i in range(machine_num):
    basic_price.append(random.randint(1,10))
    time_price.append(random.randint(1,5))
    machine_time.append(0)
print("basic_price: ", basic_price)
print("time_price: ", time_price)
print("machine_time: ", machine_time)

print("请输入job的数量,以回车结束")
job_num = int(input())
processing_time = []
print("随机产生每个job的processing time")
for i in range(job_num):
    processing_time.append(random.randint(1,10))
print("processing_time: ", processing_time)

for i in range(job_num):
    iindex = machine_time.index(min(machine_time))
    machine_time[iindex] += processing_time[i]
    print("job "+str(i+1)+" 在machine "+str(iindex+1)+" 上处理")
    print("处理job "+str(i+1)+"之后每台机器加工时间为: ", machine_time)
    
print("Cmax = ", max(machine_time))
total_cost = 0
total_cost += sum(basic_price)
for i in range(machine_num):
    total_cost += time_price[i] * machine_time[i]
print("total_cost = ", total_cost)


