from MoveGenerator import MoveGenerator
from FileHandler import FileHandler
from heapq import heappop,heappush
from operator import itemgetter
from copy import deepcopy
import tkinter as tk
from tkinter import filedialog
def a_star(mg,h):
    """well, we need to search states and be able to pass the current state and possible next states to h then update cur, 
    format is (bk,wk,wr)  """
    cur=(mg.bk,mg.wk,mg.wr) #current state
    P={} #parent dictionary
    counter=0 #SEXP
    Q=[(h(None,cur),None,cur)] #heuristic based priority queue :)
    while counter<=10000 and Q: #10,000
        d,p,cur=heappop(Q)
        mg.wk,mg.wr=cur[1],cur[2] #this update not done in mg so we have to do here
        if cur in P: continue #we ain't gonna repeat moves in a way we get to earlier board config
        P[cur]=p #set parent pointer
        mg.wkScope,mg.wrScope=[],[] #clear em
        mg.whitePossibleMoves() #fill em
        king=deepcopy(mg.wkScope)
        rook=deepcopy(mg.wrScope)
        mg.adjustWhitemove() #properly mov em basing on current black king location
        rook,mg.wrScope=mg.wrScope,rook #swap em back so that black moves properly
        king,mg.wkScope=mg.wkScope,king
        blacks_move=mg.bkMovegen() #updates mg.bk ,mg.bkScope checks if game's over
        #if cur[0]==cur[2]:
        #    cur=(blacks_move,cur[1],cur[2])
        #    if cur not in P:
        #        P[cur]=p
        if mg.theend==True: return P,cur,counter #black can't move so we just return and check in main wether it's stalemate or checkmate note: scope issues maybe
        mg.wkScope=deepcopy(king) #safely get back the adjusted values
        mg.wrScope=deepcopy(rook)
        next_states=[(blacks_move,k,cur[2]) for k in mg.wkScope]+[(blacks_move,cur[1],r) for r in mg.wrScope] #only one white piece can move but not both
        counter+=len(next_states) #SEXP update
        Q=[] #i think we need to clear Q too
        for nxt in next_states:
            heappush(Q,(h(cur,nxt),cur,nxt))
        next_states=[] #must clear it, no use keeping anyway
    return P,cur,counter #game dosen't end we still gotta return what we did


def h(prev,nxt):
    """ going to take current and next board configs (cuz we know where the black king gon' move) and drop in a lower
        number for the better one"""
    val=500
    if prev is not None: #poor design you got a branch just to accomodate
        mini=max([(0,abs(prev[0][1]-5)),(1,abs(prev[0][0]-5))],key=itemgetter(1))[0] # 0 is y - axis 1 is x axis
        if mini==0: #minimize y dist maximize x dist, do we need to maximize x we won't get killed anyway , or minimize both let's see
            val-=25*(abs(prev[0][1]-prev[2][1])-abs(nxt[0][1]-nxt[2][1]))
        elif mini==1:
            val-=25*(abs(prev[0][0]-prev[2][0])-abs(nxt[0][0]-nxt[2][0]))
        b=max(abs(prev[0][0]-prev[1][0]),abs(prev[0][1]-prev[1][1]))
        a=max(abs(nxt[0][0]-nxt[1][0]),abs(nxt[0][1]-nxt[1][1]))
        val-=12*(b-a) # cuz we want a<=b so, a-b<=0 so b-a is bigger and will reduce more :)
        return val
    else:
        return 2000 #make sure initial state is never popped out again

if __name__=='__main__':
    root=tk.Tk()
    root.withdraw()
    file_path=filedialog.askopenfilename()
    fh=FileHandler(file_path)
    fh.readFile()
    with open('output.txt','a') as output_file:
        print(fh.testcases,file=output_file) #number of games
    remap={} #remap coordinates so they make sense in output , p.s indexing from zero now
    l=[(y,x) for x in range(1,9) for y in range(1,9)]
    p=[(x,y) for x in range(7,-1,-1) for y in range(8)]
    for t1,t2 in zip(l,p):
        remap[t1]=t2
    for z in range(fh.testcases): #use z to index fh.train_num
        mg=MoveGenerator(fh.getInitialState())
        #if initial state is unsafe for our pieces we save em and then throw em into a* cuz you'll never make unsafe moves again
        normal_flag=True
        safety_first=False
        initial_board_config=(mg.bk,mg.wk,mg.wr)
        black_set=set(mg.bkScope)
        if mg.wk in black_set: #special case need not even call a_star
            path=[]
            mg.wk=mg.bk #just kill the idiot
            path.append((mg.bk,mg.wk,mg.wr))
            path.append(initial_board_config)
            sexp=1
            normal_flag=False
        else:
            if mg.wr in black_set:
                mg.whitePossibleMoves()
                rook_list=list(set(mg.wrScope).difference(black_set)) #let us move our rook closer to our king for safety :)
                m=[abs(mg.wk[0]-x[0])+abs(mg.wk[1]-x[1]) for x in rook_list]
                mg.wr=rook_list[m.index(min(m))]
                mg.bk=mg.bkMovegen()
                safety_first=True
            mg.wrScope=[]
            mg.wkScope=[]
            parent,last,sexp=a_star(mg,h)
            path=[last]
            while parent[last] is not None:
                path.append(parent[last])
                last=parent[last]
            if safety_first:
                path.append(initial_board_config)
        board=[['--' for x in range(8)] for y in range(8)]
        with open('output.txt','a') as output_file:
            print(fh.train_num[z],file=output_file)
            print('Akshay',' ',len(path)-1,' ',sexp,file=output_file) #name number_of_white_moves sexp
            while path:
                tt=path.pop() # bk tt[0],wk tt[1],wr tt[2]
                try:
                    board[remap[tt[0]][0]][remap[tt[0]][1]]='BK'
                    board[remap[tt[1]][0]][remap[tt[1]][1]]='WK'
                    board[remap[tt[2]][0]][remap[tt[2]][1]]='WR'
                    for row in board:
                        print(" ".join(c for c in row),file=output_file)
                    board[remap[tt[0]][0]][remap[tt[0]][1]]='--'
                    board[remap[tt[1]][0]][remap[tt[1]][1]]='--'
                    board[remap[tt[2]][0]][remap[tt[2]][1]]='--'
                except KeyError:
                    pass
                print('\n',file=output_file)
            if normal_flag:
                print(mg.gameEnds(),file=output_file) #not needed for submission just for you to see now"""
            else:
                print('checkmate',file=output_file)
            print('\n',file=output_file)



        






    
    

        


            

        






    






