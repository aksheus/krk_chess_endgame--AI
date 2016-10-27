class FileHandler:
	"""read input from file and provide states
	   read state sequence and print out output file"""
	def __init__(self,filename):
		self.filename=filename
		self.testcases=0
		self.train_num=[] #list or single value let it be list for now 
		self.content=None #check1

	def readFile(self):
		with open(self.filename) as input_file:
			self.content=input_file.readlines() 
		self.testcases=int(self.content[0].strip()) #check2
		self.content=self.content[1:]

	def getInitialState(self):
		if self.content!=[]:
			lines10=self.content[:10]
			initial_state=[]
			self.train_num.append(str(self.content[0].strip()))
			lines10=lines10[1:-1]
			y=8
			def pairwise(iterable):
				a=iter(iterable)
				return zip(a,a)
			for line in lines10:
				s=list("".join(line.split())) # s of form '----BK----' spaces and new lines gone ##CHECK SCOPE##
				l=[]
				for u,v in pairwise(s):
					l.append(u+v)
				#check for list index return value use try except here get positions for 
				#WK, BK and WR and add them to initial_state and return it 
				try:
					if 'BK' in l:
						initial_state.append((l.index('BK')+1,y))
					if 'WR' in l:
						initial_state.append((l.index('WR')+1,y,'R'))
					if 'WK' in l:
						initial_state.append((l.index('WK')+1,y,'K'))
				except ValueError:
						pass
				y-=1
			self.content=self.content[10:] #awesome so far
			#we have to make sure bk is first
			return [m for m in initial_state if len(m)==2]+[n for n in initial_state if len(n)==3]
		else:
			return 'no more file content'

	



		


