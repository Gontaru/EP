import random
import math
#struct evolution program
#begin
#t<-0
#initializa P(t)
#evaluate P(t)
	#while(not termination-condition) do
	#begin
		#t<-t+1
		#select P(t) from P(t-1)
		#alter P(t)
		#evaluate P(t)
	#end
#end


#esta es la distancia máxima posible que usaremos como referencia para evaluar el camino entre 2 ciudades
max_dis=100*math.sqrt(2)
pm=0.1
OPTION=1


def distance(c1,c2):
    return (math.sqrt( pow(abs(c2.x-c1.x),2) + pow(abs(c2.y-c1.y),2)))

#Función para evaluar cada miembro de la población
def eval(list,clist):
	e=0
	for i in range (len(list)):
		if(i<len(list)-1): e = ((max_dis - distance(clist[list[i]],clist[list[i+1]])) / max_dis) + e
		else: e = ((max_dis - distance(clist[list[0]],clist[list[i]])) / max_dis) + e
	return e


def mutate(c):
	pos1=random.randint(0,len(c)-1)
	pos2=random.randint(0,len(c)-1)
	while(pos1==pos2):
		pos1=random.randint(0,len(c)-1)
		pos2=random.randint(0,len(c)-1)
	aux=c[pos1]
	c[pos1]=c[pos2]
	c[pos2]=aux

def crossover(l1,l2,fl):
	nc=[-1] * len(l1)
	ini=random.randint(0,len(l1)-1)
	fin=random.randint(0,len(l1)-1)
	while(ini==fin):
		ini=random.randint(0,len(l1)-1)
		fin=random.randint(0,len(l1)-1)

	auxpos=0

	if(fin<ini):
		k=ini
		ini=fin
		fin=k
		k=0
	
	i=ini
	#copiamos el substring del primer padre en el hijo
	while True:
		nc[i]=l1[i]
		i=i+1
		if(i>fin): break

	#rellenamos el hijo con el orden relativo del segundo padre
	for j in range(len(nc)):
			if(nc[j]==-1):
				for k in range(len(l2)):
					if(nc.count(l2[k])==0 and ((j<ini or j>fin))):
						nc[j]=l2[k]
						j=j+1

	while(nc.count(-1)!=0):
		c = random.randint(0,len(l1)-1)
		if(nc.count(c)==0):nc[nc.index(-1)]=c
	#print("HIJO RESULTANTE"+str(nc))
	m=random.uniform(0.00,1.00)
	if(m<pm):
		mutate(nc)
	fl.append(nc)
	return nc

def co(l1,l2):
	pos=random.randint(0,len(l1)-1)
	for i in range(len(l1)):
		if(i<pos):
			l1[i]=l2[i]
		else:
			l2[i]=l1[i]
	m=random.uniform(0.00,1.00)
	if(m<pm):
		mutate(l1)
	m=random.uniform(0.00,1.00)
	if(m<pm):
		mutate(l2)


class city:
	def __init__(self,xp,yp,n):
		self.x=xp
		self.y=yp
		self.number=n

	def tostring(self):
		print("Ciudad nº: "+str(self.number)+" con coord(x,y): ("+str(self.x)+", "+str(self.y)+")")

def main():
	pc=0.25
	ncities=0;
	cities_list=[]
	eval_list=[]
	best_tour=[]
	new_generation=[]
	q_list=[]
	p_list=[]
	F=0
	#for i in range(10):
	#	x = random.randint(0,100)
	#	y = random.randint(0,100)
	#	c = city(x,y,ncities)
	#	ncities=ncities+1;
	#	cities_list.append(c)
	#	c.tostring()
	cities_list.append(city(95, 1,0))	
	cities_list.append(city(45, 99,1))
	cities_list.append(city(95, 17,2))
	cities_list.append(city(90, 52,3))
	cities_list.append(city(97, 71,4))
	cities_list.append(city(72, 97,5))
	cities_list.append(city(16, 70,6))
	cities_list.append(city(24, 58,7))
	cities_list.append(city(60, 92,8))
	cities_list.append(city(91, 20,9))

	initial_tours = []
	for i in range(10):
		initial_tours.append([])
		closed_tour=False
		while closed_tour==False:
			auxc = random.randint(0,9)
			if((auxc in initial_tours[i])==False): initial_tours[i].append(auxc)
			if(len(initial_tours[i])==10): closed_tour=True
	
	optimo_local=0
	prueba=[0,2,9,3,4,5,8,1,6,7]
	print("PROBANDO: "+ str(eval(prueba,cities_list)))
	for i in range(len(initial_tours)):
		eval_list.append(eval(initial_tours[i],cities_list))
	for i in range(len(initial_tours)):
		if(optimo_local<eval_list[i]):
				optimo_local=eval_list[i]
				best_tour=initial_tours[i]




	i=0
	if(OPTION==0):
		while(i<40):
			i=i+1
			parents_list=[]
			for j in range(len(initial_tours)):
				c = random.uniform(0.00,1.00)
				if(c<pc):
					parents_list.append(initial_tours[j])
			for j in range(len(parents_list)):
				if(j<len(parents_list)-1):
					new_generation.append(crossover(parents_list[j],parents_list[j+1],initial_tours))
			for j in range(len(new_generation)):
				eval_list.append(eval(new_generation[j],cities_list))
			for j in range(len(eval_list)):
				if(optimo_local<eval_list[j]):
					optimo_local=eval_list[j]
					best_tour=initial_tours[j]
			new_generation=[]
	else:
		for j in range(len(initial_tours)):
			p_list.append(eval(initial_tours[j],cities_list))
		for j in range(len(initial_tours)):
			if(optimo_local<p_list[j]):
					optimo_local=p_list[j]
					best_tour=initial_tours[j]	
		i=0
		while(i<3000):
			parents_list=[]
			q_list=nc=[0]*len(p_list)
			i=i+1
			#Obtenemos F y la probabilidad de selección p para cada individuo
			for j in range(len(initial_tours)):
				F = F + p_list[j]
			for j in range(len(initial_tours)):
				for k in range(j):
					q_list[j] = q_list[j] + p_list[k]
			for j in range(len(eval_list)):
				selected = False
				r = random.uniform(0.00,1.00)
				aux=0
				#if(initial_tours[j]==optimo_local):
				#	new_generation.append(initial_tours[j])
				#	selected=True
				while selected==False:
					if(r<p_list[aux]):
						new_generation.append(initial_tours[aux])
						selected=True
					aux=aux+1			
			for j in range(len(new_generation)):
				c = random.uniform(0.00,1.00)
				if(c<pc):
					parents_list.append(new_generation[j])
			for j in range(len(parents_list)):
				if(j<len(parents_list)-1):
					co(parents_list[j],parents_list[j+1])
			p_list=[]
			for j in range(len(new_generation)):
				p_list.append(eval(new_generation[j],cities_list))
			initial_tours=[]
			initial_tours=new_generation
			for j in range(len(p_list)):
				if(optimo_local<p_list[j]):
					optimo_local=p_list[j]
					best_tour=initial_tours[j]
			new_generation=[]
	print("SOLUCION ENCONTRADA "+str(best_tour) +" con valor: "+str(optimo_local))
main()




