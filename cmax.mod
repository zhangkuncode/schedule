/*********************************************
 * OPL 12.9.0.0 Model
 * Author: zk
 * Creation Date: Aug 10, 2019 at 9:17:19 PM
 *********************************************/

/* 紧界的例子
int p[JobNum] = [7,7,6,6,5,5,4,4,4];
int a[MachineNum] = [1,1,1,1]; // 基础费用
int b[MachineNum] = [1,1,1,1]; // 单位费用
*/

 
//using CP; 使用这个回报错,具体原因不清楚，可能优化引擎变了

int job_num = 50;
int machine_num = 10;

range JobNum = 1..job_num;
range MachineNum = 1..machine_num;

int p[JobNum] =   [20, 20, 20, 19, 19, 18, 18, 17, 17, 17, 16, 16, 16, 16, 15, 15, 15, 15, 14, 14, 13, 13, 12, 12, 11, 10, 10, 10, 10, 10, 10, 10, 10, 9, 8, 8, 8, 8, 8, 7, 6, 6, 6, 5, 5, 4, 4, 3, 2, 2];

int a[MachineNum] =   [7, 6, 6, 9, 2, 1, 2, 10, 4, 5]; // 基础费用
int b[MachineNum] = [4, 1, 1, 4, 3, 4, 1, 2, 5, 2]; // 单位费用
float buget_cost =    1197.55; // 预算价格

dvar int x[MachineNum][JobNum] in 0..1;
dvar int y[MachineNum] in 0..1;
dvar int makespan;

minimize makespan;

subject to { // 只能写作用于决策变量的布尔表达式。用于说明模型的约束条件
//if-else 语句中的条件必须是基本条件；即，它们不得包含决策变量。 也不得包含 forall 语句
/*  下面一个约束就够了，不需要2个
    forall (i in MachineNum){ // 机器循环
    ct0:
      (sum(j in JobNum) x[i][j] ) > (y[i]-1)*maxint;
  }  
*/
  forall (i in MachineNum){ // 机器循环
    ct_machine:
      ( (sum(j in JobNum) (x[i][j])) - y[i]*maxint ) <= 0;// big M解决if else问题
  }   
  
  ct_buget:
  ( (sum(i in MachineNum) (y[i]*a[i])) + sum(i in MachineNum) (sum(j in JobNum) (b[i]*p[j]*x[i][j])) ) <= buget_cost;
 
 
  forall (j in JobNum){
    ct_nonpreemption:
    	(sum(i in MachineNum) x[i][j]) == 1;
  }   
 
  forall (i in MachineNum){
    ct_makespan:
    	sum(j in JobNum) (p[j]*x[i][j]) <= makespan;
  }
}

