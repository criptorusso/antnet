# -*- coding: utf-8 -*-
"""
@autor: Antonio Russoniello
"""

import networkx as nx
import matplotlib.pyplot as plt
import random


############ VARIABLES GLOBALES ################
#escenarios exitosos: 500 hormigas y 10 nodos, 700 hormigas y 20 nodos
#num_hormigas = 100 #recomendado por Dorigo num_hormigas = n^50 n=longitud del recorrido
num_hormigas = 700
nodo_origen = 1
alfa = 2 # importancia de feromonas
beta = 3 # peso de las distancias (mayor distancia =  mayor costo = peor caso))
# ciclo_corrida = 100
ciclo_corrida = 200
tau_inicial = 0.01
tau_incr = 0.10
#num_nodos = 10 # numero de Nodos
num_nodos = 20
nodo_destino = num_nodos - 1


############ CLASE HORMIGAS ################
class Hormigas:

    def __init__(self, grafo, indice_hormiga, nodo_actual):
        self.indice = indice_hormiga
        self.grafo = grafo
        self.nodo_actual = nodo_actual
        self.ttl = num_hormigas * ciclo_corrida
        self.nodos_visitados = []
        self.nodos_visitados.append(nodo_actual)
        self.loop = False
        
    def quien_soy(self):
        if(self.nodo_actual != nodo_destino):   
            print 'soy hormiga: ', self.indice
            print 'estoy en nodo: ', self.nodo_actual
            print 'vecinos del nodo actual: ', self.grafo.edges(self.nodo_actual)
        else:
            print 'soy hormiga: ', self.indice
            print 'llegue a destino: ', self.nodo_actual
            #print 'soy una hormiga muerta :-('
            print 'mis nodos visitados son: ', self.nodos_visitados
            self.ttl = 1
        if (self.loop):
            print 'estoy atrapada en un loop' 
            
        
    def proximo_nodo(self):
        while (self.nodo_actual != nodo_destino):
            self.lista_prob = []
            self.lista_prob2 = []
            self.rango_prob = []
            self.sumatoria = 0
            self.aristas = self.grafo[self.nodo_actual]
            #print 'nodo actual ', self.nodo_actual
            self.nodos_vecinos = self.aristas.keys() 
            #print len(self.aristas)
            print 'vecinos ', self.nodos_vecinos
            self.nodos_vecinos = self.eliminar_repeticiones(self.nodos_vecinos, self.nodos_visitados)
            if (len(self.nodos_vecinos) == 0):
                self.loop = True
                print 'estoy atrapada en un loop'                
                break            
            for i in range(len(self.nodos_vecinos)):
                self.feromona = self.grafo[self.nodo_actual][self.nodos_vecinos[i]]['tau']
                self.distancia = self.grafo[self.nodo_actual][self.nodos_vecinos[i]]['distancia']
                print '++++++++++  nodo %i  ++++++++++++' % self.nodos_vecinos[i]
                print '++      feromona %f '      % self.feromona
                print '++      distancia %f '     % self.distancia
                #self.prob = ((self.feromona)**alfa)*((self.distancia)**beta) # para favorecer distancias grandes
                self.prob = ((self.feromona)**alfa)*((1-self.distancia)**beta) #para favorecer distancias pequeñas
                if (self.prob == 0):
                    self.prob = 0.01 
                print '++      probabilidad %f '  % self.prob
                
                self.sumatoria = self.sumatoria + self.prob
                #print self.grafo.edges(self.indice)
                #print 'sumatoria; ', self.sumatoria
                self.lista_prob.append(self.prob)
            for i in range(0, len(self.nodos_vecinos)):
                #print lista_prob[i]
                self.lista_prob2.append(round((self.lista_prob[i]/self.sumatoria),5))
                if (i == 0):
                    self.rango_prob.append([0,self.lista_prob2[i]])
                    self.rango_inf = self.lista_prob2[i]
                else:
                    self.rango_sup = self.rango_inf + self.lista_prob2[i]
                    self.rango_prob.append([self.rango_inf, self.rango_inf + self.lista_prob2[i]])
                    self.rango_inf = self.rango_inf + self.lista_prob2[i]
            print '++++++++++++++++++++++++++++++++'
            print 'probabilidad por arista: ', self.lista_prob2
            print 'rango de probabilidades: ', self.rango_prob
            self.valor_aleatorio = random.uniform(0,1)
            print 'valor aleatorio: ', self.valor_aleatorio
        
            for j in range(len(self.nodos_vecinos)):
                self.nodo_actual = j
                if ((self.valor_aleatorio >= self.rango_prob[j][0]) & (self.valor_aleatorio <= self.rango_prob[j][1])):
                    break               

            print 'proximo nodo a visitar: ', self.nodos_vecinos[self.nodo_actual]
            
            self.nodos_visitados.append(self.nodos_vecinos[self.nodo_actual])
            print 'nodos visitados: ', self.nodos_visitados
            self.nodo_actual = self.nodos_vecinos[self.nodo_actual]
            return            
    
    def actualizar_feromonas(self):
        sum_distancias = 0
        for i in range(0, len(self.nodos_visitados)-1):
            print 'arista %s <-> %s: ' % (self.nodos_visitados[i], self.nodos_visitados[i+1])
            print 'tau: ', self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau']
            # sumar todos los costos de la ruta y el inverso sera el tau incremental aplicado a cada arista
            print 'distancia: ',  self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['distancia']
            sum_distancias = sum_distancias + self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['distancia']          
        # actualizacion de feromonas para la ruta    
        #print sum_distancias
        delta_tau = 1/sum_distancias
        for i in range(0, len(self.nodos_visitados)-1):
            tau_actual = self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau']
            self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau'] = round((tau_actual + delta_tau), 2)
        print 'tau actualizado: ', self.grafo[self.nodos_visitados[i]][self.nodos_visitados[i+1]]['tau']
        return
        
    def eliminar_repeticiones(self, nodos_ve, nodos_vi):
        self.vecino = set(nodos_ve)
        self.visitado = set(nodos_vi)
        self.conjunto = self.vecino- self.visitado
        print 'lista de nodos sin repeticiones ', list(self.conjunto)
        return list(self.conjunto)
        
    def tiempo_vida(self):
        if (self.ttl > 1):        
            self.ttl = self.ttl - 1
            #print 'tiempo restante de vida: ', self.ttl
        return self.ttl
    
    def hormiga_back():
        return

############ GRAFICAR GRAFO ################
def graficar_grafo(graph, labels, graph_layout, node_color, edge_color):
    node_size=350
    node_alpha=.8
    node_text_size=12
    edge_alpha=.5
    edge_tickness=3
    #edge_text_pos=0.3
    text_font='sans-serif'
    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)    
    # draw graph
    nx.draw_networkx_nodes(graph, graph_pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(graph, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(graph, graph_pos, font_size=node_text_size, font_family=text_font)
    for arista in graph.edges():
        dict = {arista: graph.edge[arista[0]][arista[1]]['distancia']}
        nx.draw_networkx_edge_labels(graph,graph_pos, dict, label_pos=0.3)
    plt.axis('off')    
    plt.show()

           
########################## INICIO ############################################
# crear grafo con atributo etiqueta
G = nx.Graph(etiqueta="grafo")
G.add_nodes_from(range(1,num_nodos+1))

# Generar Grafo con distancias conocidas para DEBUG
#for i in range(1,num_nodos+1):
#    for s in range(1,3):    
#        G.add_edge(i,random.randint(1,num_nodos), distancia=0.1, tau=round(tau_inicial, 2))
#        labels = (chr, range(1,num_nodos))


# Generar Grafo con valores aleatorios de distancia
for i in range(1,num_nodos+1):
    for s in range(1,3):       # garantiza de dos a tres nodos conectados
        G.add_edge(i,random.randint(1,num_nodos), distancia=round(random.uniform(0,1),2), tau=tau_inicial)
        labels = (chr, range(1,num_nodos))

print('Componentes conectados:')
print(sorted(nx.connected_components(G), key = len, reverse=True))
#print 'grado del ultimo nodo:', G.degree(num_nodos) # mostrar grado del ultimo elemento
#print 'aristas del ultimo nodo:', G.edges(num_nodos) # mostrar aristas del ultimo nodo


# Graficar grafo
#graficar_grafo(G,labels=True, graph_layout='shell', node_color='red', edge_color='green')

# Definir Ruta a optimizar
#nodo_origen = raw_input('Nodo origen: ')
#nodo_destino= raw_input('Nodo destino: ')
#ruta_corta = nx.shortest_path(G, source=int(nodo_origen), target=int(nodo_destino))
#print 'ruta mas corta: ', ruta_corta, '\n'
for i in range(1, len(G)+1):
    print 'Nodo:', i
    print 'Nodos Adyacentes: ', G[i]
    
print '\nInicio de Colonia de Hormigas'
print 'Cantidad de Hormigas: ', num_hormigas
# crear lista de hormigas
hormigas_lista = [ Hormigas(G, i, nodo_origen) for i in range(num_hormigas)]

ciclos = 0
while (ciclos < ciclo_corrida):
    for i in range(len(hormigas_lista)):
        print '================================================'    
        hormigas_lista[i].quien_soy()    
        hormigas_lista[i].proximo_nodo()
        hormigas_lista[i].tiempo_vida()
    print '\n* Resultados Parciales:'
    for i in range(1, len(hormigas_lista)):
        if (hormigas_lista[i].loop == False):
            print '\nhormiga %i actualizando feromona para nodos visitados: %s' % (i, hormigas_lista[i].nodos_visitados)
            hormigas_lista[i].actualizar_feromonas()
       
    ciclos += 1

print '\n* Resultados Finales:'

lista_rutas = []
lista_rutas_unicas = []
contar_ruta = 0
for i in range(1, len(hormigas_lista)):
    if (hormigas_lista[i].loop == False):
        print '\nhormiga %i ruta: %s' % (i, hormigas_lista[i].nodos_visitados)
        contar_ruta = lista_rutas.count(hormigas_lista[i].nodos_visitados)
        lista_rutas.append(hormigas_lista[i].nodos_visitados)    
        if ( contar_ruta > 0):
            ruta_existe_flag = True
        else:
            ruta_existe_flag = False
            lista_rutas_unicas.append(hormigas_lista[i].nodos_visitados)
print '\n'
costo_ruta = 0
lista_costos = []
for ruta in lista_rutas_unicas:
    print 'ruta %s seleccionada %s veces' % (ruta, lista_rutas.count(ruta))
    for i in range(0, len(ruta)-1):
        costo_ruta = costo_ruta + G[ruta[i]][ruta[i+1]]['distancia']
    lista_costos.append(round(costo_ruta,2))
    print 'costo ruta %s igual a %s ' % (ruta, costo_ruta)
    indice = lista_costos.index(min(lista_costos))

print '\nla ruta %s tiene el menor costo (%s) ' % (lista_rutas_unicas[indice], min(lista_costos))
       
#   lista_rutas.count(lista_rutas_unicas[0])

#        if (lista_rutas.count(hormigas_lista[i].nodos_visitados) == 0):
#            continue
#        else:
#            lista_rutas.append(hormigas_lista[i].nodos_visitados)





    # ejemplo imprimir distancia y tau de aristas conectadas 1-4  G[1][4]['tau']
    # asignar un nuevo valor al atributo    G[1][2]['tau'] = 4.7