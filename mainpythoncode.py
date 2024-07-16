import numpy as np

'''
세대 위치.
에너지
유전자(형질)

우열 
여러가지 그래프

시간에 따른 패널티가 없으면(늙지 않으면)조상 세대가 자원을 지속적으로 소비하여 종의 성장을 방해
'''

genesize = 4

energy_ch = [
    [0.002, [[0, [ 1, 1, 1]]]],
	[0.003, [[0, [-1,-1, 1]]]],
	[0.006, [[1, [ 1,-1, 1]], [2, [-1,-1, 1]]]],
	[0.006, [[1, [ 1,-1,-1]], [3, [ 1, 1, 1]]]],
]

atmosphere = [
	[1000, 10],
	[1000, 10],
	[1000, 20],
	[1000, 20],
]

class Creature:
	def __init__(self, ancestor_creature, generation_position, energy, gender, genes):
		self.ancestor_creature	= ancestor_creature
		self.generation_position= generation_position
		self.energy				= energy
		self.gender				= gender
		self.genes				= genes

		self.time = 0

	def EVENT(self):
		atmosphere_ = atmosphere
		
		self.energy -= 1+self.time*0.001
		self.time += 1

		for num in range(len(energy_ch)):
			True_ = 0
			for ch in energy_ch[num][1]: 
				if [n-(n**2)+1 for n in self.genes[ch[0]]] == ch[1]: True_ += 1

			if len(energy_ch[num][1]) == True_:
				energy_ = atmosphere[num][0]*energy_ch[num][0]
				self.energy += energy_
				atmosphere_[num][0] -= energy_
		
		return atmosphere_


creatures = []
creatures.append(Creature(0, 0, 50, 0, [[ 0,-1, 1], [ 1,-1, 0], [ 1,-1, 1], [ 0, 0, 0]]))
creatures.append(Creature(1, 0, 50, 1, [[ 1, 0,-1], [ 0,-1, 1], [ 1, 0,-1], [ 1,-1,-1]]))
creatures.append(Creature(2, 0, 50, 0, [[ 0, 0, 1], [ 0,-1,-1], [ 1,-1, 0], [ 1, 0, 1]]))
creatures.append(Creature(3, 0, 50, 1, [[-1,-1, 0], [ 0, 0, 1], [ 0,-1,-1], [ 0,-1,-1]]))

while True:
	for creature in creatures:
		print(f"{creature.gender}, {creature.generation_position}, {creature.energy:.1f}, {creature.genes}")

	input()
	for _ in range(1):
		mature_creature = []

		for creature in creatures: 
			atmosphere = creature.EVENT()

			if creature.energy < 0: 
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

			genes_ = []
			for i in range(len(genesize)):
				gene_1 = [np.random.choice([-1, 1]) if n == 0 else n for n in mature_creature[0].genes[i]]
				gene_2 = [np.random.choice([-1, 1]) if n == 0 else n for n in mature_creature[1].genes[i]]
				


			genes				= [[[mature_creature[0].genes[i], mature_creature[1].genes[i]][np.random.randint(2)], 
									np.random.choice([-1, 0, 1], 3, replace = True)][np.random.choice(2, p=[0.85, 0.15])]
									for i in range(genesize)]
				
			
			mature_creature[0].energy = 50
			mature_creature[1].energy = 50

			creatures.append(Creature(ancestor_creature, generation_position, energy, gender, genes))

		for atmosphere_ in atmosphere:
			atmosphere_[0] += atmosphere_[1]
		
