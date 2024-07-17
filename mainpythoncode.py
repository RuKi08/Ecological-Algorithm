import sys
import numpy as np
from matplotlib import pyplot as plt

'''
세대 위치.
에너지
유전자(형질)

우열 
여러가지 그래프

시간에 따른 패널티가 없으면(늙지 않으면)조상 세대가 자원을 지속적으로 소비하여 종의 성장을 방해
'''

genesize = 4
gene_Tx = 'AaBbCcDdEeFfGgHhIiJjKkLl'

energy_ch = [
    [0.002, [[0, [ 1, 1, 1]]]],
	[0.003, [[0, [-1,-1, 1]]]],
	[0.006, [[1, [ 1,-1, 1]], [2, [-1,-1, 1]]]],
	[0.006, [[1, [ 1,-1,-1]], [3, [ 1, 1, 1]]]],
]

atmosphere_Tx = ['A', 'B', 'C', 'D']

atmosphere = [
	[1000, 10],
	[1000, 10],
	[1000, 20],
	[1000, 20],
]

graph_atmosphere = [[], [], [], []]
graph_creatures = []
graph_creatures_energy_ch = [[], [], [], []]
graph_creatures_energy_ch_bar = [0, 0, 0, 0]
sex_ratio = []


class Creature:
	def __init__(self, ancestor_creature, generation_position, energy, gender, genes):
		self.ancestor_creature	= ancestor_creature
		self.generation_position= generation_position
		self.energy				= energy
		self.gender				= gender
		self.genes				= genes

		self.time = 0

		self.energy_acquisition_num = []

		for num in range(len(energy_ch)):
			True_ = 0
			for ch in energy_ch[num][1]: 
				if [n-(n**2)+1 for n in genes[ch[0]]] == ch[1]: True_ += 1

			if len(energy_ch[num][1]) == True_:
				self.energy_acquisition_num.append(num)


	def EVENT(self):
		atmosphere_ = atmosphere
		
		self.energy -= 1+self.time*0.001
		self.time += 1

		for num in self.energy_acquisition_num:
			energy_ = atmosphere[num][0]*energy_ch[num][0]
			self.energy += energy_
			atmosphere_[num][0] -= energy_
	
		return atmosphere_

ancient_creatures = []

creatures = []
creatures.append(Creature(0, 0, 50, 0, [[ 0,-1, 1], [ 1,-1, 0], [ 1,-1, 1], [ 0, 0, 0]])) 
creatures.append(Creature(1, 0, 50, 1, [[ 1, 0,-1], [ 0,-1, 1], [ 1, 0,-1], [ 1,-1,-1]]))
creatures.append(Creature(2, 0, 50, 0, [[ 0, 0, 1], [ 0,-1,-1], [ 1,-1, 0], [-1, 0, 1]]))
creatures.append(Creature(3, 0, 50, 1, [[-1,-1, 0], [ 0, 0, 1], [ 0,-1,-1], [ 0,-1,-1]]))

stageSize = 1

while True:
	# for creature in creatures:
	# 	print(f"{creature.gender}, {creature.generation_position}, {creature.energy:.1f}, {creature.genes}")

	TEXT = input('\033[33mCommand_ \033[0m')

	try:
		family_tree = [[] for _ in range(max([i.generation_position for i in creatures])+1)]
	except ValueError: 
		family_tree = [[] for _ in range(max([i.generation_position for i in ancient_creatures])+1)]
		
	try:
		for creature in ancient_creatures:
			family_tree[creature.generation_position].append(creature)

		for creature in creatures:
			family_tree[creature.generation_position].append(creature)
	except:
		print('\033[31mError\033[0m')
		

	if TEXT.isdecimal(): stageSize = int(TEXT)
	elif TEXT == 'print':
		for Y in range(len(family_tree)):
			print()
			print(f'\033[96m{Y}\033[0m', end='\t')
			for X in range(len(family_tree[Y])):
				Tx = ''
				for i in family_tree[Y][X].energy_acquisition_num:
					Tx += atmosphere_Tx[i]


				if family_tree[Y][X] in creatures: 	print(f'\033[0m{X}_{Tx}\033[0m', end='\t')
				else:								print(f'\033[90m{X}_{Tx}\033[0m', end='\t')

		print()
		continue
	elif TEXT == 'reset':
		creatures = []
		creatures.append(Creature(0, 0, 50, 0, [[ 0,-1, 1], [ 1,-1, 0], [ 1,-1, 1], [ 0, 0, 0]]))
		creatures.append(Creature(1, 0, 50, 1, [[ 1, 0,-1], [ 0,-1, 1], [ 1, 0,-1], [ 1,-1,-1]]))
		creatures.append(Creature(2, 0, 50, 0, [[ 0, 0, 1], [ 0,-1,-1], [ 1,-1, 0], [-1, 0, 1]]))
		creatures.append(Creature(3, 0, 50, 1, [[-1,-1, 0], [ 0, 0, 1], [ 0,-1,-1], [ 0,-1,-1]]))

		ancient_creatures = []
		continue

	#부모, 세대, 섭취 에너지, 유전자형
	elif 'get' in TEXT:
		try:
			index = TEXT.replace('get ', '').split('_')
			creature = family_tree[int(index[0])][int(index[1])]

			energy_tx = []
			for i in creature.energy_acquisition_num:
				energy_tx.append(atmosphere_Tx[i])

			parent_1 = f'{creature.ancestor_creature[0].generation_position}_{family_tree[creature.ancestor_creature[0].generation_position].index(creature.ancestor_creature[0])}'
			parent_2 = f'{creature.ancestor_creature[1].generation_position}_{family_tree[creature.ancestor_creature[1].generation_position].index(creature.ancestor_creature[1])}'

			gene_Tx_ = ''
			for i in range(genesize):
				for l in range(3):
					if creature.genes[i][l] == -1:
						gene_Tx_ += gene_Tx[(i*3+l)*2+1]*2
					elif creature.genes[i][l] == 1:
						gene_Tx_ += gene_Tx[(i*3+l)*2]*2
					else:
						gene_Tx_ += gene_Tx[(i*3+l)*2] + gene_Tx[(i*3+l)*2+1]

			print('\033[96m------------------------\033[0m')
			print(f'\033[96mGeneration\t\033[0m{creature.generation_position}')
			print(f'\033[96mParent\t\t\033[0m{parent_1}, {parent_2}')
			print(f'\033[96mEnergy\t\t\033[0m{", ".join(energy_tx)}')
			print(f'\033[96mGenotype\t\033[0m{gene_Tx_}')
			print('\033[96m------------------------\033[0m')
		except:
			print('\033[31mError\033[0m')
		continue
	elif TEXT == 'show':
		# 총 에너지량
		# 각각 에너리쟝
		# 총 개체수
		# 분해능력 별 개체수
		# 성비
		# 분해능력 별 개체수 막대그래프
		graph_creatures_energy_ch_bar = [0, 0, 0, 0]
		sex_ratio = []
		 
		plt.scatter(3, 2, 1)
		graph__ = graph_atmosphere[0]
		for graph in graph_atmosphere[1:]:
			for i in range(len(graph)): graph__[i] += graph[i]
		plt.plot(graph__)
		plt.ylim(0, 10000)

		plt.scatter(3, 2, 2)
		for graph in graph_atmosphere:
			plt.plot(graph)
			plt.ylim(0, 5000)

		plt.scatter(3, 2, 3)
		plt.plot(graph_creatures)

		plt.scatter(3, 2, 4)
		for graph in graph_creatures_energy_ch:
			plt.plot(graph)

		plt.scatter(3, 2, 5)
		plt.bar(graph_creatures_energy_ch_bar)

		plt.scatter(3, 2, 6)
		plt.plot(sex_ratio)
		plt.plot([1-i for i in sex_ratio])
		
		plt.show()
		continue

	elif TEXT == 'exit': 
		sys.exit()
	else: continue

	for _ in range(stageSize):
		mature_creature = []

		for creature in creatures: 
			atmosphere = creature.EVENT()

			if creature.energy < 0: 
				ancient_creatures.append(creature)
				creatures.remove(creature)
				continue

			if creature.energy > 100: #에너지가 충분한가

				if mature_creature == []: # 비었는가 
					mature_creature.append(creature)

				elif creature.gender != mature_creature[0].gender: # 성별이 다른가 
					if creature.ancestor_creature != mature_creature[0].ancestor_creature: # 부모가 다른가
						mature_creature.append(creature)

		if len(mature_creature) > 1:
			ancestor_creature 	= [mature_creature[0], mature_creature[1]]
			generation_position = np.max([mature_creature[0].generation_position, mature_creature[1].generation_position]) +1
			energy				= 50
			gender				= np.random.randint(2)

			gene_ = []
			for i in range(genesize):
				gene_1 = [np.random.choice([-1, 1]) if n == 0 else n for n in mature_creature[0].genes[i]]
				gene_2 = [np.random.choice([-1, 1]) if n == 0 else n for n in mature_creature[1].genes[i]]

				gene_.append([(gene_1[i] + gene_2[i])/2 for i in range(3)])
				
			genes = [[gene_[i], np.random.choice([-1, 0, 1], 3, replace = True)][np.random.choice(2, p=[0.85, 0.15])] for i in range(genesize)]
				
			
			mature_creature[0].energy = 50
			mature_creature[1].energy = 50

			creatures.append(Creature(ancestor_creature, generation_position, energy, gender, genes))

		for NUM in range(len(atmosphere)):
			graph_atmosphere[NUM].append(atmosphere[NUM][0])
			atmosphere[NUM][0] += atmosphere[NUM][1]

		sex_ratio_Num = [0, 0]
		graph_creatures.append(len(creatures))

		for i in graph_creatures_energy_ch: i.append(0)
		for creature in creatures:
			for i in range(len(graph_creatures_energy_ch_bar)):
				if creature.energy_acquisition_num in i: 
					graph_creatures_energy_ch[i][-1] += 1
					graph_creatures_energy_ch_bar[i] += 1

			if creature.gender == 0:sex_ratio_Num[0] += 1
			else: 					sex_ratio_Num[1] += 1

		sex_ratio.append(sex_ratio_Num[0]/(sex_ratio_Num[0]+sex_ratio_Num[1]))
		

# %%
