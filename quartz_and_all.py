import json
from os import listdir
import csv
import numpy as np
import matplotlib.pyplot as plt
import pprint
import pandas as pd
import matplotlib.patches as mpatches

pp = pprint.PrettyPrinter(indent=4)


class QuartzAndAll(object):
	df = None

	def plotHazardsCounter(self, target_products, optimised=''):
		"""This methods shows a plot of the hazards in the project"""
		hazards_types_counter = {}
		hazards_types_counter = {'purple': 0, 'red': 0, 'orange': 0, 'unknown': 0}
		for file in listdir('quartz'):
			if file != '.DS_Store' and file.split('.')[0] in target_products:
				with open('./quartz' + optimised + '/' + file, 'rU') as json_file:
					product = json.load(json_file)
					for color in product['health']['hazards']:
						hazards_types_counter[color] +=1

		n_groups = 4

		X = (hazards_types_counter['purple'], hazards_types_counter['red'],
			hazards_types_counter['orange'], hazards_types_counter['unknown'])

		fig, ax = plt.subplots()

		index = np.arange(n_groups)
		bar_width = 0.5

		opacity = 0.4
		error_config = {'ecolor': '0.3'}

		rects1 = plt.bar(0 + 0.25, X[0], bar_width,
						alpha=opacity,
						color='purple',
						error_kw=error_config,
						label='Purple')

		rects1 = plt.bar(1 + 0.25, X[1], bar_width,
						alpha=opacity,
						color='red',
						error_kw=error_config,
						label='Red')

		rects1 = plt.bar(2 + 0.25, X[2], bar_width,
						alpha=opacity,
						color='orange',
						error_kw=error_config,
						label='Orange')

		rects1 = plt.bar(3 + 0.25, X[3], bar_width,
						alpha=opacity,
						color='grey',
						error_kw=error_config,
						label='Unknown')

		plt.xlabel('Hazard Level')
		plt.ylabel('Count')
		plt.title('Number of hazards in project (' + str(sum(X)) + ')')
		plt.xticks(index + bar_width, ('Purple', 'Red', 'Orange', 'Unknown'))
		plt.legend()

		plt.tight_layout()
		plt.show()

	def plotHazardsHist(self, target_products, optimised=''):
		"""
		This method loads the health hazards into a dataframe. The it makes a plot
		of the health hazards in the project. Each dot represents a product hazard.
		a hazard from a product.

		If you open this file with the python interpreter (execfile), you will be 
		able fo play with the Dataframe for further research.
		"""
		s_hazard = {'lightgrey': 50, 'purple': 5000, 'red': 400, 'orange': 100}

		data = {'values': [],
		'color': [],
		's': [],
		'color_id': [],
		'hazard_id': [],
		'hazard_name': [],
		'product_name': []}

		products = {}
		hazards_names = {}
		colors = ['purple', 'red', 'orange', 'unknown', 'lightgrey']
		for file in listdir('quartz'):
			if file != '.DS_Store' and file.split('.')[0] in target_products:
				with open('./quartz' + optimised + '/' + file, 'rU') as json_file:
				#with open('./quartz/' + file, 'rU') as json_file:
					product = json.load(json_file)
					for color in product['health']['hazards']:
						for hazard in product['health']['hazards'][color]:
							try:
								hazards_names[hazard['name']] += 1
							except Exception, e:
								hazards_names[hazard['name']] = 1

							data['product_name'].append(product['name'])
							data['hazard_name'].append(hazard['name'])
							data['color_id'].append(colors.index(color))
							if color == 'unknown':
								color = 'lightgrey'
							data['color'].append(color)
							data['s'].append(s_hazard[color])
							data['values'].append(hazard['massPct'] * 100)

		# print pp.pprint(products)
		# print pp.pprint(data)
		h_names = hazards_names.keys()
		for i, h_name in enumerate(data['hazard_name']):
			data['hazard_id'].append(h_names.index(h_name))

		df = pd.DataFrame(data)
		self.df = df
		# Show the head of the Dataframe
		print df.sort_values(['hazard_id', 'values'], ascending=[True, False]).head()

		# Print some general stats
		print 'mean {} std {}'.format(df['values'].mean(),df['values'].std())
		ax1 = plt.subplot(111)

		# Add the data to the plot
		for color, y, x,s in zip(df['color'].values, df['hazard_id'].values, df['values'].values,df['s'].values):
			ax1.scatter(y, x, s=s, c=color)

		# Add legend
		purple = mpatches.Patch(color='purple', label='Very Bad')
		red = mpatches.Patch(color='red', label='Bad')
		orange = mpatches.Patch(color='orange', label='Still Bad')
		surprise = mpatches.Patch(color='lightgrey', label='Surprise!')

		# Add some other stuff to make it look nice & shiny
		plt.xlabel("Hazard Name, each dot represent a product's hazard")
		plt.ylabel('Hazard level (%)')
		plt.title('Health & Safety Hazards in Project Before')
		plt.xticks(range(len(hazards_names)), hazards_names, rotation='vertical')
		plt.legend(handles=[purple, red, orange, surprise])
		ax1.set_ylim(ymin=-3)
		ax1.set_xlim(xmin=-0.5)
		plt.tight_layout()
		plt.subplots_adjust(bottom=0.4)
		plt.show()

		# return df, usefule for if you want to use the python interpreter to do
		# further research
		return df

	def quarts2ProductsAndManufacturers(self):
		"""
		This methods generate search queries in order to map from quartz to
		products from real manufacturers. We used SpecifiedBy's and Google as a
		source of building product informations
		"""
		items = []
		for file in listdir('quartz'):
			if file != '.DS_Store':
				with open('./quartz/' + file, 'rU') as json_file:
					item = {}
					f = json.load(json_file)
					item['name'] = f['name']
					item['search_query'] = [f['name']]
					item['CPID'] = f['CPID']
					item['quartz_url'] = 'http://quartzproject.org/p/' + item['CPID']
					item['potential_products'], item['potential_manufacturers'], item['potential_manufacturers_google'] = [], [], []

					if item['name']:
						potential_product = 'https://www.specifiedby.com/search?q=' + f['name']
						potential_manufacturer = 'https://www.specifiedby.com/search?q=' + f['name'] + '&type=companies&a=0'
						potential_manufacturer_google = 'https://www.google.co.uk/search?q=' + f['name'] + ' companies&type=companies&a=0'

						item['potential_products'].append(potential_product)
						item['potential_manufacturers'].append(potential_manufacturer)
						item['potential_manufacturers_google'].append(potential_manufacturer_google)

					for altName in f['altNames']:
						if altName:
							item['search_query'].append(altName)
							potential_product = 'https://www.specifiedby.com/search?q=' + altName
							item['potential_products'].append(potential_product)

							potential_manufacturer = 'https://www.specifiedby.com/search?q=' + altName + '&type=companies&a=0'
							item['potential_manufacturers'].append(potential_manufacturer)

							potential_manufacturer_google = 'https://www.google.co.uk/search?q=' + altName + ' companies&type=companies&a=0'
							item['potential_manufacturers_google'].append(potential_manufacturer_google)

					items.append(item)

		with open('quartz2products_and_manufacturers.csv', 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['name', 'search_query', 'quartz_url', 'CPID', 'potential products',
				'potential manufacturers', 'potential manufacturers google'])

			for item in items:
				# print item
				for i in range(len(item['potential_products'])):
					writer.writerow([item['name'], item['search_query'][i], item['quartz_url'], item['CPID'], item['potential_products'][i],
						item['potential_manufacturers'][i], item['potential_manufacturers_google'][i]])
		
	def createRankedListToMitigate(self):
		self.df.sort_values(['color_id', 'values'],ascending=[True, False]).to_csv('./ranked_list_of_hazards_to_mitigate.csv')

if __name__ == '__main__':
	target_product_ids = ['CP005-a00', 'CP179-a00', 'CP109-a00', 'CP131-a00', 'CP129-a00', 'CP170-a00',
	'CP152-a00', 'CP150-a00', 'CP173-a00', 'CP150-a00', 'CP042-a01',
	'CP072-a01', 'CP071-a00', 'CP126-a00']
	target_product_ids_optimised = ['CP179-a00', 'CP109-a00', 'CP131-a00',
	'CP129-a00', 'CP152-a00', 'CP150-a00', 'CP173-a00', 'CP150-a00', 'CP042-a01',
	'CP072-a01', 'CP071-a00', 'CP126-a00']
	qA = QuartzAndAll()
	qA.plotHazardsCounter(target_product_ids,)
	# qA.plotHazardsCounter(target_product_ids_optimised, '_optimised')
	df = qA.plotHazardsHist(target_product_ids)
	# df = qA.plotHazardsHist(target_product_ids_optimised, '_optimised')
	qA.createRankedListToMitigate()
	#qA.quarts2ProductsAndManufacturers()