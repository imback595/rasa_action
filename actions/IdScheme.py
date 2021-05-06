
from py2neo import Graph,Node,Relationship

graph=Graph("http://localhost:7474",auth=("neo4j","123456"))


def get_id_scheme(text,Id):

    if text  in ['乳腺癌']:
        match='match(disease:Disease{name:"%s"})-[]->(next) return next.name ,ID(next)'%(disease)
        rrr='match(disease:Disease{name:"%s"})-[next_question]->()  return type(next_question)'
        data = graph.run(match).data()
        data2 = graph.run(rrr).data()
        return data,data2

    else:
        hhh ='match(a)-[]->(next) where ID(a)=%d   return next.name,ID(next)  '%(Id)

        rrr=  'match(a)-[next_question]->()  where ID(a)=%d   return type(next_question)'%(Id)



        data = graph.run(hhh).data()
        data2=  graph.run(rrr).data()
        return data,data2



if __name__=='__main__':
    next_name,next_question=get_id_scheme('乳腺癌',0)
    print(next_name)
    print(next_question)







