class MoveGenerator:
	"""
	         state=(BK,WK,WR)--> state=((x,y),(x,y,R),(x,y,K)) check for K and R for whose values most likely order you get is bk,w
	         where wk , wr and bk are positions for the pieces
    """
	def __init__(self,state): 
		self.state=state #represennts initial state of the game p.s state is list not tuple
		self.bk=state[0] #current black king position
		if state[1][2]=='R':
			self.wr=state[1][:-1]
		elif state[1][2]=='K':
			self.wk=state[1][:-1]
		if state[2][2]=='K':
			self.wk=state[2][:-1]
		elif state[2][2]=='R':
			self.wr=state[2][:-1]
		self.adj_king=[(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
		self.wrScope=[] #possible moves for rook and king 
		self.wkScope=[]
		self.bkScope=[]
		for x,y in self.adj_king:
			temp=(self.bk[0]+x,self.bk[1]+y)
			if temp[0]<9 and temp[0]>0:
				if temp[1]<9 and temp[1]>0:
					self.bkScope.append(temp)
		self.theend=False
		#shall we make wrScope,wkScope and bkScope sets for efficiency ?? Let's see 
		#I think onlybkScope can be made a set ..wkscope and wrscope need to be iterable hmm..
 
	def bkMovegen(self):
		""" first priority is to capture an uprotected rook , else  move to safe field, 
		    no safe field the game ends"""
		# FULL AWESOME
		self.bkScope=[]
		for x,y in self.adj_king:
			temp=(self.bk[0]+x,self.bk[1]+y)
			if temp[0]<9 and temp[0]>0:
				if temp[1]<9 and temp[1]>0:
					self.bkScope.append(temp)	#this should do it :)
		k= lambda x,y: (abs(x-5)*5)+(abs(y-5)*3)+((x+y)*0.1)
		self.bkScope=[(x,y,k(x,y)) for x,y in self.bkScope]
		self.bkScope.sort(key=lambda n: n[2])
		self.bkScope=[(x,y) for x,y,z in self.bkScope] #already sorted do not need those values anymore
		#first priority attack white rook if safe
		"""	we do not need this if self.wr in self.bkScope: 
			if self.wr not in self.wkScope:
				return self.wr #kills the rook #do not update self.bk here cuz you are not gonna let it attack anyway"""
		#make safe move 
		#assume game ends if bk can't move
		self.theend=True
		if self.wr in self.bkScope:
			self.bkScope.remove(self.wr)
		for t in self.bkScope:
			if t not in self.wrScope:
				if t not in self.wkScope:
					self.bk=t
					self.theend=False #game dosen't end and afterall
					break
		if self.theend==False:
			return self.bk
		else:
			return 'call gameEnds'
			#call gameends method

	def whitePossibleMoves(self):
		"""there's a catch wk and wr can't occupy each others positions unless the rook is under attack THE SUBTLE BUG, INTERDEPENDENCY
		you don't need to do this check right yet , do it just before the white pieces move cuz it's affecting BK behavior
		if self.wr in self.wkScope:
			self.wkScope.remove(self.wr)
		if self.wk in self.wrScope:
			self.wrScope.remove(self.wk) """
		for i in range(1,9):
			if i!=self.wr[0]:
				self.wrScope.append((i,self.wr[1]))
			if i!=self.wr[1]:
				self.wrScope.append((self.wr[0],i))
		for x,y in self.adj_king:
			temp=(self.wk[0]+x,self.wk[1]+y)
			if temp[0]<9 and temp[0]>0:
				if temp[1]<9 and temp[1]>0:
					self.wkScope.append(temp)
		#we need to trim rooks possible moves as it can't run through the other pieces
		#first consider white king along horizontal aka y axis is same
		trim=[z for z in self.wrScope if z[1]==self.wk[1]]
		if trim!=[]: #which means white king is there horizontally 
			if self.wk[0]>self.wr[0]: #check if king is to the left or right of the rook
				trim=[z for z in trim if z[0]>self.wk[0]] #remember we are removing !!!
			elif self.wk[0]<self.wr[0]:
				trim=[z for z in trim if z[0]<self.wk[0]] #this means king is to the left so whatever is left of the king exclude it
			for tr in trim:
				try:
					self.wrScope.remove(tr)
				except ValueError:
					pass
		#second consider white king along vertical axis i.e. x axis is same
		trim=[z for z in self.wrScope if z[0]==self.wk[0]]
		if trim!=[]: #which means white king is there vertically 
			if self.wk[1]>self.wr[1]: #check if king is above or below the rook
				trim=[z for z in trim if z[1]>self.wk[1]]
			elif self.wk[1]<self.wr[1]:
				trim=[z for z in trim if z[1]<self.wk[1]]
			for tr in trim:
				try:
					self.wrScope.remove(tr)
				except ValueError:
					pass
		if self.bk[0]==self.wr[0] or self.bk[1]==self.wr[1]: #rook should be able to attack the black king
			if self.bk not in self.wrScope:
				self.wrScope.append(self.bk)


	def gameEnds(self):
		""" check for check/stale mate and other end game functionality later to be added :)"""
		if self.bk in self.wkScope or self.bk in self.wrScope:
			return'checkmate'
		else:
			return'stalemate'

	#black king behavior successfuly debugged 
	def adjustWhitemove(self): #some preprocessing must call before the search
		#similarly for black king horizontal
		trim=[z for z in self.wrScope if z[1]==self.bk[1]]
		if trim!=[]: #which means white king is there horizontally 
			if self.bk[0]>self.wr[0]: #check if king is to the left or right of the rook
				trim=[z for z in trim if z[0]>self.bk[0]] #remember we are removing !!!
			elif self.bk[0]<self.wr[0]:
				trim=[z for z in trim if z[0]<self.bk[0]] #this means king is to the left so whatever is left of the king exclude it
			for tr in trim:
				try:
					self.wrScope.remove(tr)
				except ValueError:
					pass
		#similarly black king vertical
		trim=[z for z in self.wrScope if z[0]==self.bk[0]]
		if trim!=[]: #which means white king is there vertically 
			if self.bk[1]>self.wr[1]: #check if king is above or below the rook
				trim=[z for z in trim if z[1]>self.bk[1]]
			elif self.bk[1]<self.wr[1]:
				trim=[z for z in trim if z[1]<self.bk[1]]
			for tr in trim:
				try:
					self.wrScope.remove(tr)
				except ValueError:
					pass
		if self.wr in self.wkScope:
			self.wkScope.remove(self.wr)
		if self.wk in self.wrScope:
			self.wrScope.remove(self.wk) 
		#they can't run into each other 
		#either pices shouldn't be in the neighborhood of bk without backup
		full_bkscope=[]
		for x,y in self.adj_king:
			temp=(self.bk[0]+x,self.bk[1]+y)
			if temp[0]<9 and temp[0]>0:
				if temp[1]<9 and temp[1]>0:
					full_bkscope.append(temp)
		to_remove=[r for r in self.wrScope if r in full_bkscope and r not in self.wkScope]
		self.wrScope=[x for x in self.wrScope if x not in to_remove]
		self.wkScope=[x for x in self.wkScope if x not in full_bkscope] #we can't lose our king backup or not
		#except for first move wk,wr are aware of their safety before search, not first move cuz bkscope not available yet
		#be careful to consider this in your search algorithm/heuristic
		










