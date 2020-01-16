import time
import sys
PLACE_HOLDER = '_'

class npprefix: 
    prefix1 = []
    prefix2 = []
    prefix3 = []

def read(filename):
    S = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            elements = line.split(',')      #分隔符
            s = []
            for e in elements:
                s.append(e.split())
            S.append(s)
    return S
    
class SquencePattern:
    def __init__(self, squence, support):
        self.squence = []
        for s in squence:
            self.squence.append(list(s))  #元组换成列表
        self.support = support
    def add(self, p):                           #如果第一位是‘_’则remove后再加到squence里面
        if p.squence[0][0] == PLACE_HOLDER:
            first_e = p.squence[0]
            first_e.remove(PLACE_HOLDER)
            self.squence[-1].extend(first_e)
            self.squence.extend(p.squence[1:])
        else:
            self.squence.extend(p.squence)
        self.support = min(self.support, p.support)

     
        
def NprefixSpan(pattern, S, threshold):#S为三维数组
    patterns = []
    f_list = get_frequent_items(S, pattern, threshold)
    for i in f_list:        
        p = SquencePattern(pattern.squence, pattern.support)
        p.add(i)
        patterns.append(p)
        p_S = build_projected_database(S, p) #p_S就是投影数据库
        ###print("p.squence:%s" % p.squence)
        ###print("p_S:%s" % p_S)
        p_patterns = NprefixSpan(p, p_S, threshold)  #将递归得到的频繁模式加进总模式中
        patterns.extend(p_patterns)
    return patterns

def get_frequent_items(S, pattern, threshold):#获得频繁项集
    items = {}
    _items = {}
    f_list = []
    if S is None or len(S) == 0:
        return []
        
    for s in S:     #S表示所有行三维数组，s表示单一行二维数组 ##S表示4维数组，s表示单一行三维数组
        #class 1
        break_flag = False
        ###print("_______s = %s" % s)
        if PLACE_HOLDER in s[0][0]:       #计算support值,如果有_,计算_之后的元素的support
            #print("有_________________________________________________")
            for item in s[0][1:][0]:#for i,item in enumerate(s[0][1:]):
                if item in ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
                    if item in _items:
                        _items[item] += 1
                    else:
                        _items[item] = 1
                    ###print("_items[%s]= %d" %(item,_items[item]))
                else:###if item in ['a','b','c','d','e','f','g','h']
                    for sequence in pattern.squence:
                        if item.upper() in sequence:
                            if item in _items:
                                _items[item] += 1
                                ###print("_items[%s]= %d" %(item,_items[item]))
                                break_flag = True
                            else :
                                _items[item] = 1
                                ###print("_items[%s]= %d" %(item,_items[item]))
                                break_flag = True
                            if break_flag == True:
                                break
                if break_flag == True:
                    break
            s = s[1:]#####删除第一个
        # class 2
        break_flag2 = False
        counted = []
        for element in s:
            for item in element:
                if item[0] in ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
                    if item[0] not in counted:
                        counted.append(item[0])
                        if item[0] in items :      
                            items[item[0]] += 1
                        else:
                            items[item[0]] = 1
                        ###print("items[%s]= %d" %(item[0],items[item[0]]))
                else:
                    for sequence in pattern.squence:
                        ###print("sequence = %s" %sequence)
                        if item[0].upper() in sequence:
                            if item[0] not in counted:
                                counted.append(item[0])
                                if item[0] in items : 
                                    items[item[0]] += 1
                                    ###print("items[%s]= %d" %(item[0],items[item[0]]))
                                    break_flag2 = True
                                else:
                                    items[item[0]] = 1
                                    ###print("items[%s]= %d" %(item[0],items[item[0]]))
                                    break_flag2 = True
                                if break_flag2 == True:
                                    break
                if break_flag2 == True:
                    break
            if break_flag2 == True:
                break
    f_list.extend([SquencePattern([[PLACE_HOLDER, k]], v) for k, v in _items.items() if v >= threshold]) #进行support比较，此为带_型
    f_list.extend([SquencePattern([[k]], v) for k, v in items.items() if v >= threshold])  #进行support比较，此为不带_型
    #print(f_list)
    sorted_list = sorted(f_list, key=lambda x: x.support)    #lambda是虚拟函数,x换成p也没问题，x指f_list，根据support的小大排序f_list
    return sorted_list

def build_projected_database(S, pattern):   ####改变数据库的递归顺序

    # print(S)
    # print(pattern.squence)

    p_S = []
    last_e = pattern.squence[-1]
    last_item = last_e[-1]##不用变
    
    ###print("pattern.squence:%s" % pattern.squence)
    ###print("last_e:%s" % last_e)
    ###print("last_item:%s" % last_item)
    
    for s in S:
        temp_pattern = []
        for element in s:##element = ['_05','C05']
            ###print("element:%s" % element)
            is_prefix = False
            ####
            #for item in element:##item = 'B05'
            if PLACE_HOLDER == element[0][0]:##item[0] = 'B'
                for t1 in element:##t1 = '_05'  'C05'
                    if t1[0] == last_item and len(last_e) > 1:
                        is_prefix = True
                        break##可有可无??
            else:
                #is_prefix = True
                for item in last_e:####item = 'e' 'a'
                    for t2 in element:##t2 = '_05'  'C05'
                        if item == t2[0]:
                            is_prefix = True
                            break##可有可无？？                   
                    break
            ###print("is_prefix:%d" % is_prefix)            
            if is_prefix:
                e_index = s.index(element)##index无影响
                num1 = 0##索引
                for t3 in element:##t3 = '_05'  'C05'
                    if t3[0] == last_item:
                        i_index = num1
                    else:
                        num1 += 1
                ##i_index = element.index(last_item)
                if i_index == len(element) - 1:#如果是最后一个
                    temp_pattern = s[e_index + 1:]#删掉这个元素及其之前的元素，取之后的
                else:
                    temp_pattern = s[e_index:]#删掉这个元素之前的元素，取它及其之后的
                    # index = element.index(last_item)
                    temp_e = element[i_index:]#把这个元素里的这个字符及其之后的字符设为temp_e
                    #print("temp_e:%s" % temp_e)
                    s_temp_e = list(temp_e[0])
                    #print("s_temp_e:%s" % s_temp_e)                    
                    s_temp_e[0] = PLACE_HOLDER
                    #print("s_temp_e:%s" % s_temp_e)
                    temp_e[0] = ''.join(s_temp_e)
                    #print("temp_e[0]:%s" % temp_e[0])
                    #temp_e[0][0] = _#把这个字符换成_
                    temp_pattern[0] = temp_e
                break
            #
            #
            ###print("temp_pattern:%s" % temp_pattern)
        if len(temp_pattern) != 0:
            p_S.append(temp_pattern)
    return p_S


def filter_patterns(patterns):
    new_patterns = []
    for p in patterns:
        dict = {'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'G':0,'H':0,'I':0,'J':0,'K':0,'L':0,'M':0,
                'N':0,'O':0,'P':0,'Q':0,'R':0,'S':0,'T':0,'U':0,'V':0,'W':0,'X':0,'Y':0,'Z':0,}
        for item in p.squence:
            for element in item:
                if element in ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
                    dict[element] += 1
                else:
                    dict[element.upper()] -= 1
            judge = True
            for count in dict.values():
                if count != 0:
                    judge = False
        if judge == True:
            new_patterns.append(p)
            #print("pattern:{0}, support:{1}".format(p.squence, p.support))
    #for i in new_patterns:
        #print("pattern:{0}, support:{1}".format(i.squence, i.support))
    return new_patterns
    

def print_patterns(S, S2, patterns):
    count = 0
    for p in patterns:
        if len(p.squence) > 2:##########################################################长度最小限制###########
            count += 1
            # print("{0}.模式:{1}, 出现次数:{2}".format(count, p.squence, p.support))
            S2.write("{0}.模式:{1}, 出现次数:{2}\n".format(count, p.squence, p.support))#####
            npprefix.prefix1.append(p.squence)
            get_time(S, S2, p.squence)
    #A灯 B门 C空调 D电视 E热水器 F扫地机器人 
    b1 = '灯07:20开，灯11:56关，电视16:43开，热水器19:00开，热水器20:33关，电视22:13关'
    b2 = '灯07:20开，灯11:56关，电视16:43开，电视22:13关'
    b3 = '灯07:20开，灯11:56关，热水器19:00开，热水器20:33关'
    b4 = '门05:27开，门09:52关，电视14:32开，热水器16:50开，热水器18:42关，电视20:10关'
    b5 = '门05:27开，门09:52关，电视14:32开，电视20:10关'
    b6 = '门05:27开，门09:52关，热水器16:50开，热水器18:42关'
    b7 = '电视14:32开，热水器16:50开，热水器18:42关，电视20:10关'
    npprefix.prefix3 = [(b1, b1),
                        (b2, b2), (b3, b3), (b4, b4), (b5, b5), (b6, b6), (b7, b7)]
    # print("模式个数为:%d" % count)
    S2.write("模式个数为:%d\n" % count)
    return npprefix

def get_time(S, S2, squence):        
    time = {}
    length = len(squence)
    #print("squence:%s" % squence)
    #print("length:%d" % length)
    for i in range(length):
        time[i] = []
    #print("time:%s" % time)
    for s1 in S:
        #print("s1:%s" % s1)
        count = 0
        temp_time = {}
        for s2 in s1:           
            #print("s2:%s" % s2)
            #print("s2[0][0]:%s" % s2[0][0])
            '''if s2[0][0] == squence[count][0]:####s2[0][0]解决原序列中有多个
                temp_time[count]= s2[0][1:]
                count += 1'''
            for s3 in s2:    
                if s3[0] == squence[count][0]:
                    temp_time[count] = s3[1:]
                    count += 1
                    #print("count:%d" % count)  
                    break
            if count == length:    ###全部符合就记录           
                for k,v in temp_time.items():
                    time[k].append(v)
                #print("done")
                #print("time:%s" % time)  
                break             
                #print("temp_time:%s" % temp_time)
    for k,v in time.items():
        time[k].sort()##########排序
    #print("time:%s" % time)
    #S2.write("time:%s\n" % time)

    
    ave_time = {}
    get_ave(time, ave_time)

    # print("ave_time:%s" % ave_time)
    npprefix.prefix2.append(ave_time)
    #S2.write("ave_time:%s\n" % ave_time)
    
    recommend_time(time, ave_time)    #np4.5
    #print("time:%s" % time)
    #S2.write("time:%s\n" % time)
###########################新时间    
    new_time = {}
    for i in range(len(time)):
        if(len(time[i])>= 2):
            #print((time[i][0]))
            new_time[i] = []
            new_time[i].append(time[i][0])
            if(time[i][-1] != time[i][0]):
                new_time[i].append(time[i][-1])
        elif(len(time[i]) == 1):
            new_time[i] = []
            new_time[i].append(time[i][0][0]+time[i][0][1]+':'+time[i][0][2]+time[i][0][3])
        else:
            new_time[i] = ['无合适时间']
#############################新时间2
    new_time2 = {}
    for i in range(len(new_time)):
        if(len(new_time[i]) == 2):
            new_time2[i] = []
            new_time2[i].append(new_time[i][0][0]+new_time[i][0][1]+':'+new_time[i][0][2]
            +new_time[i][0][3]+'-'+new_time[i][1][0]+new_time[i][1][1]+':'+new_time[i][1][2]
            +new_time[i][1][3]) 
        else:
            new_time2[i] = new_time[i]
            #new_time2[i] = []
            #new_time2[i].append(new_time[i][0][0]+new_time[i][0][1]+':'+new_time[i][0][2]+new_time[i][0][3])
          
    #print("推荐时间:%s" % new_time2)
    S2.write("推荐时间:%s\n" % new_time2)
    
###################################      
    #print("____________________________________________")
    S2.write("____________________________________________\n")
    
    
def recommend_time(time, ave_time):
    for i in range(len(time)):
        for j in range(len(time[i])):
            #print(time[i][j])
            #print(ave_time[i])
            a = time[i][j]
            b = ave_time[i]
            sum1 = int(a[0])*600 + int(a[1])*60  + int(a[2])*10 + int(a[3])
            sum2 = int(b[0])*600 + int(b[1])*60  + int(b[2])*10 + int(b[3])
            if (abs(sum1 - sum2)>120):###################################时间过滤限制##################################
                time[i][j] = 'null' 
                #if 
    for i in range(len(time)):
        c = time[i].count('null')
        if c > 0:
            for j in range(c):
                time[i].remove('null')
    #print(time)    
    #new_time = time
    #for k,v in time.items():

def get_ave(time, ave_time):
    for k,v in time.items():
        length2 = len(v)
        sum = 0
        #print("length2:%d" % length2)
        #print("v:%s" % v)
        #v = [int(x) for x in v]
        for a in v:
            sum = sum + int(a[0])*600 + int(a[1])*60  + int(a[2])*10 + int(a[3])
        #print("sum:%d" % sum)
        ave = int(sum/length2)
        n1 = int(ave/600)
        #print("n1:%d" % n1)
        s1 = ave % 600
        #print("s1:%d" % s1)
        n2 = int(s1/60)
        #print("n2:%d" % n2)
        s2 = s1 % 60
        #print("s2:%d" % s2)
        n3 = int(s2/10)
        #print("n3:%d" % n3)
        s3 = s2 % 10
        #print("s3:%d" % s3)
        last = str(n1) + str(n2) + str(n3) + str(s3)
        #print("last:%s" % last)
        ave_time[k] = last    
        
        



