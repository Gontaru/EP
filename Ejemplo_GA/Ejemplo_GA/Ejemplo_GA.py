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
pc=0.25


def distance(c1,c2):
    return (math.sqrt( pow(abs(c2.x-c1.x),2) + pow(abs(c2.y-c1.y),2)))

#Función para evaluar cada par miembros de la población
#cuánto menor sea la distancia entre dos ciudades, mayor será el valor devuelto
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


def selectng(ng,it,ql):

	for o in range(len(ql)):
		selected = False
		r = random.uniform(0.00,ql[len(ql)-1])
		aux=0
		while selected==False and aux<len(ql):
			if(r<ql[aux]):
				ng.append(it[aux])
				selected=True
			aux=aux+1

def eval_population(it, el, cl, F, ql, pl):
	F=0
	ol=0
	bt=[0]*len(it)
	#Evaluamos la poblacion
	for j in range(len(it)):
		el[j] = eval(it[j],cl)
		if(ol<el[j]):
			ol=el[j]
			bt=it[j]
	#Obtenemos F
	for k in range(len(it)):
		F = F + el[k]

	#Calculamos la probabilidad pi de selección para cada individuo
	for l in range(len(it)):
		pl[j]=	(el[l]	/	F)

	#Calculamos la probabilidad cumulativa para cada individuo, 
	#siendo {q0 = eval0, q1=eval0 + eval1, ... , qn = eval0 + eval1 + ... evaln}
	for m in range(len(it)):
		for n in range(m):
			ql[m] = ql[m] + pl[n]

	return ol, bt

def generate_offsprings(ng,pi,pl,cl):
	for p in range(len(ng)):
			c = random.uniform(0.00,1.00)
			if(c<pc):
				#añadimos los padres que posteriormente realizarán el cruce
				pi.append(p)
				pl.append(ng[p])
			for q in range(len(pl)):
				if(q<len(pl)-1):
					ng[pi[q]]=(crossover(pl[q],pl[q+1], cl))

def main():
	ncities=0;
	PROBLEM_SIZE=20;
	cities_list=[]
	eval_list=[]
	best_tour=[]
	new_generation=[]
	q_list=[]
	p_list=[]
	F=0

	#inicializamos las ciudades (espacio de búsqueda)
	for i in range(PROBLEM_SIZE):
		x = random.randint(0,100)
		y = random.randint(0,100)
		c = city(x,y,ncities)
		ncities=ncities+1;
		cities_list.append(c)
		c.tostring()

	#inicializamos soluciones aleatorias (nº individuos)(Hay que sustituirlo por problem_size)
	initial_tours = []
	for i in range(PROBLEM_SIZE):
		initial_tours.append([])
		closed_tour=False
		while closed_tour==False:
			auxc = random.randint(0,PROBLEM_SIZE-1)
			if((auxc in initial_tours[i])==False): initial_tours[i].append(auxc)
			if(len(initial_tours[i])==PROBLEM_SIZE): closed_tour=True
		print(str(initial_tours[i]))
	
	#asignamos el optimo local
	optimo_local=0

		
	eval_list=q_list=p_list=[0]*len(initial_tours)

	#evaluamos la poblacion inicial
	#				it,				el,			cl,			F, ql,	pl,			ol,			bt
	optimo_local, best_tour = eval_population(initial_tours, eval_list, cities_list, F, q_list, p_list)

	i=0
	while(i<10000):
		
		i=i+1
		
		#Seleccionamos los individuos para la nueva generación
		#new generation es la nueva generacion dónde añadiremos los seleccionados
		#initial_tours es dónde seleccionaremos los individuos de la actual generacion
		#q_list es la lista de probabilidades cumulativas
		selectng(new_generation,initial_tours,q_list)

		parent_index=[]		
		parent_list=[]
		#Generamos los posibles cruces que darán los descendientes de la nueva generación
		generate_offsprings(new_generation, parent_index, parent_list, cities_list)

		#asignamos la nueva generación
		initial_tours=[]
		initial_tours=new_generation
		new_generation=[]
		
		
		#Evaluamos la poblacion nueva
		aux_ol, aux_bt = eval_population(initial_tours, eval_list, cities_list, F, q_list, p_list)
		if(aux_ol>optimo_local):
			optimo_local=aux_ol
			best_tour=aux_bt

	
		print("GENERACION "+str(i)+" eval: "+str(optimo_local))
	print("SOLUCION ENCONTRADA "+str(best_tour) +" con valor: "+str(optimo_local))
main()




