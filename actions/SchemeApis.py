from py2neo import Graph,Node,Relationship

# graph=Graph("http://localhost:7474",auth=("neo4j","123456"))
##

def get_Scheme(user_list):
    graph = Graph("http://192.168.168.250:7474", auth=("neo4j", "123456"))
    print(user_list)

    for i,o in enumerate(user_list):
        if isinstance(o,list):
            user_list[i]=o[0]
    num=len(user_list)
    match_disease='match(disease:Disease{name:"%s"})'%user_list[0]
    for i,o in enumerate(user_list[1:]):
        addtext='-[r%s]->(a%s:Rela{name:"%s"})'%(i,i,o)
        match_disease=match_disease+addtext
    last_addtext='-[r%s]->(a%s)'%(num-1,num-1)
    alltype=''
    rtype_list=[]
    for i in range(0,num):
        rtype='type(r%s)'%i
        alltype=alltype+rtype+','
        rtype_list.append(rtype)
    returntext=' return  %s a%s.name '%(alltype,num-1)
    last_query=match_disease+last_addtext+returntext
    print(last_query)
    data1=graph.run(last_query).data()
    rela=[]
    value=[]


    for i in rtype_list:
        rela.append(data1[0][i])

    for  i in data1:
        value.append(i['a%s.name'%(num-1)])

    if rela[-1]=='治疗方案':
        last_query=last_query+', a%s.编码'%(num-1)
        data2=graph.run(last_query).data()
        print('----------------------')

        value2=[]
        for i in data2:

            value2.append(i['a%s.编码'%(num-1)])



        if value!=[]:
            print(value2)
            print(value)
            value=zip(value2,value)
            value=list(value)
            value=dict(value)



    return rela,value





if __name__=='__main__':


    rela,value =get_Scheme(['胃癌','转移性晚期'])

    print(rela)
    print(value)
