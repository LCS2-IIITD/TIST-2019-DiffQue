import networkx as nx
import pickle
from sklearn.svm import LinearSVR
from sklearn.neural_network import MLPClassifier
import numpy as np

st1 = "edges.txt"
st2 = "ques_pairs_with_groundtruth.txt"
st3 = "rank_nodes_pagerank_without_weight.txt"
st4 = "inverse_rankings.txt"
st5 = "time_diff.txt"
st6 = "ans_count.txt"

nooffeatures = 2
directed_graph = nx.DiGraph()
undirected_graph = nx.DiGraph()
pagerank_dict = {}
leader_fol_dict = {}
bw_centrality = {}
accepted_answer_id = {}
time_diff_of_accepted = {}

graph_file = open(st1)
for line in graph_file:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    directed_graph.add_edge(v1, v2)
    undirected_graph.add_edge(v1, v2)
    undirected_graph.add_edge(v2, v1)   
    
tested_graph_file = open(st2)
for line in tested_graph_file:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    undirected_graph.add_edge(v1, v2)
    undirected_graph.add_edge(v2, v1)

pagerank_file = open(st3)
for line in pagerank_file:
    v1 = int(line.split(" ")[0])
    pagerankk = float(line.split(" ")[1])
    pagerank_dict[ v1 ] = pagerankk
    
leader_follower_file = open(st4)
for line in leader_follower_file:
    v1 = int(line.split(" ")[0])
    leader_fol_score = float(line.split(" ")[1])
    leader_fol_dict[ v1 ] = leader_fol_score
    
time_diff_acc = open(st5)
for line in time_diff_acc:
    v1 = int(line.split(" ")[0])
    v2 = float(line.split(" ")[1])
    time_diff_of_accepted[ v1 ] = v2

answer_count = open(st6)
for line in answer_count:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    accepted_answer_id[ v1 ] = v2

def check2( vert ):
    if( vert in accepted_answer_id ):
        return accepted_answer_id[vert]
    return 0

def check3( vert ):
    if( vert in time_diff_of_accepted ):
        return time_diff_of_accepted[vert]
    return 1
    
def getfeatures(vert1, vert2):
    vect = []
    #vect.append( bw_centrality.get(vert1) )
    #vect.append( bw_centrality.get(vert2) )
    vect.append( pagerank_dict.get(vert1) )
    vect.append( pagerank_dict.get(vert2) )
    '''
    vect.append( undirected_graph.degree(vert1) )
    vect.append( undirected_graph.degree(vert2) )
    vect.append( check2(vert1) )
    vect.append( check2(vert2) )
    '''
    #vect.append( check3(vert1) )
    #vect.append( check3(vert2) )
    #vect.append( leader_fol_dict.get(vert1) )
    #vect.append( leader_fol_dict.get(vert2) )
    
    return vect
    
def preprocess():
    train_x = []
    train_y = []

    val = 0
    print('hi')
    for ed in directed_graph.edges():
        v1 = ed[0]
        v2 = ed[1]
        lab = 1

        img = getfeatures(v1, v2)
        if( None not in img ):
            val+=1
            train_x.append( img )
            train_y.append( lab )
    print( val )
    print('hi2')
    for ed in directed_graph.edges():
        v1 = ed[1]
        v2 = ed[0]
        lab = 0
        
        img = getfeatures(v1, v2)
  	
        if( None not in img ):
            train_x.append( img )
            train_y.append( lab )
     
    return train_x, train_y   
                    
train_x, train_y = preprocess()
        
trainvector = np.reshape( train_x, (len(train_x), nooffeatures) )
trainlabel = np.reshape( train_y, (len(train_y), 1) )

print('Defining')
#clf2 = LinearSVR(random_state=0)
clf2 = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,15,), random_state=1)
print('Training')
clf2.fit(trainvector, trainlabel.ravel())

print('Checking')
correct = 0
noofval = 0
rejected = 0
tested_graph_file2 = open(st2)
for line in tested_graph_file2:
    v1 = int(line.split(" ")[0])
    v2 = int(line.split(" ")[1])
    v3 = int(line.split(" ")[2])
    
    img = getfeatures(v1, v2)
    try:
        labell = clf2.predict([img])
        if( v3==v2 ):
            if( labell==1 ):
              correct += 1
        else:
            if( labell==0 ):
              correct += 1
    except Exception: 
        rejected += 1
        pass

    noofval += 1
       
print( correct, noofval, rejected )
print( (float(correct)/noofval) )
