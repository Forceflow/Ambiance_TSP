import csv
import math
import argparse
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Load places from CSV formatted as Placename, Latitude, Longitude
def parseCSV(filename):
	places = list(csv.DictReader(open(filename, newline='')))
	print("# Loaded",len(places),"places from ambiance.csv:")
	for item in places:
		print("  ", item["Place"], "|",item["Activity"], "|", item["Lat"], item["Long"])
	return places

# Extract just the coordinates (lat, long) from the places
def extractCoords(input):
	coords = []
	for item in input:
		coords.append((float(item["Lat"]), float(item["Long"])))
	return coords

# Complete a distance matrix between all locations
# (This matrix will be symmetrical) 
def compute_euclidean_distance_matrix(locations):
	# Google example uses a nested dictionary here, we upgrade it to array
	# distances = {}

	# Allocate distance matrix
	size = len(locations)
	distances = [[0 for x in range(size)] for y in range(size)]
	# Add a scaling factor (the ORTools solver only works on integers)
	scalar = 10000
	for from_counter, from_node in enumerate(locations):
		# Google example uses a nested dictionary here, we upgrade it to array
		# distances[from_counter] = {}
		for to_counter, to_node in enumerate(locations):
			if from_counter == to_counter:
				# Matrix diagonal will be zeroes
				distances[from_counter][to_counter] = 0
			else:
				x_d = (from_node[0] - to_node[0])*scalar
				y_d = (from_node[1] - to_node[1])*scalar
				distances[from_counter][to_counter] = int(math.hypot(x_d,y_d))
	return distances

# Print the original route (original order in CSV file)
def print_original_route(data, printactivities):
	original = "  "
	for item in data['places']:
		if printactivities: 
			original += '{} ({}) -> '.format(item['Place'],item['Activity'])
		else:
			original += '{} -> '.format(item['Place'])
	original+='{}'.format(data['places'][0]['Place'])
	print(original)

# Print solution to easy paste in Google Maps polyline example
def print_solution_gmaps(manager, routing, assignment, data):
	# print('Objective: {} miles'.format(assignment.ObjectiveValue()))
	index = routing.Start(0)
	print("{lat: ", data['places'][manager.IndexToNode(index)]['Lat'], ", lng: ", data['places'][manager.IndexToNode(index)]['Long'], "}, //", data['places'][manager.IndexToNode(index)]['Place'])
	while not routing.IsEnd(index):
		print("{lat: ", data['places'][manager.IndexToNode(index)]['Lat'], ", lng: ", data['places'][manager.IndexToNode(index)]['Long'], "}, //", data['places'][manager.IndexToNode(index)]['Place'])
		previous_index = index
		index = assignment.Value(routing.NextVar(index))
	# Reached the end
	print("{lat: ", data['places'][manager.IndexToNode(index)]['Lat'], ", lng: ", data['places'][manager.IndexToNode(index)]['Long'], "}, //", data['places'][manager.IndexToNode(index)]['Place'])

# Print the ORTools-generated solution
def print_solution(manager, routing, assignment, data, printactivities):
	# print('Objective: {} miles'.format(assignment.ObjectiveValue()))
	plan_output = ""
	index = routing.Start(0)
	route_distance = 0
	while not routing.IsEnd(index):
		if printactivities:
			plan_output += '{} ({}) -> '.format(data['places'][manager.IndexToNode(index)]['Place'],data['places'][manager.IndexToNode(index)]['Activity'])
		else:
			plan_output += '{} -> '.format(data['places'][manager.IndexToNode(index)]['Place'])
		previous_index = index
		index = assignment.Value(routing.NextVar(index))
		route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
	# Reached the end
	plan_output += ' {}\n'.format(data['places'][manager.IndexToNode(index)]['Place'])
	print(plan_output)

# Create a data model that can be fed to the ORTools solver
def create_data_model(csvfile):
	# Read the CSV
	places = parseCSV(csvfile)
	# Extract just the coordinates and use them to build the distance matrix
	coords = extractCoords(places)
	distancem = compute_euclidean_distance_matrix(coords)
	# Print distance matrix for sanity check
	# print(np.matrix(distancem))

	# Put all that data into a model for the ORTools solver
	data = {}
	data['places'] = places
	data['distance_matrix'] = distancem
	data['num_vehicles'] = 1
	data['depot'] = 0
	return data

def main():
	print("# Brought to you by Nerdland podcast - www.nerdland.be")
	inputfile = ""

	parser = argparse.ArgumentParser()
	parser.add_argument("csvfile", type=str, help="The path to the .csv file with the locations")
	parser.add_argument("--gmapjs", action="store_true")
	args = parser.parse_args()
	csvfile = args.csvfile

	print("# Info: Using ", csvfile, "as input for location data")
	if(args.gmapjs):
		print("# Info: Printing output as JS code for Google Maps")

	# Get all our data and setup all related model data
	data_model = create_data_model(csvfile)

	# Print original route
	print("# Original route:")
	print_original_route(data_model, True)

	# Prepare ORTools routing manager and model
	manager = pywrapcp.RoutingIndexManager(len(data_model['distance_matrix']), data_model['num_vehicles'], data_model['depot'])
	routing = pywrapcp.RoutingModel(manager)

	# Distance callback function (solver uses this to get distance costs)
	def distance_callback(from_index, to_index):
		# Convert from routing variable Index to distance matrix NodeIndex.
		from_node = manager.IndexToNode(from_index)
		to_node = manager.IndexToNode(to_index)
		return data_model['distance_matrix'][from_node][to_node]

	# Register the callback function
	transit_callback_index = routing.RegisterTransitCallback(distance_callback)
	routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

	# Configure Routing Search Parameters
	search_parameters = pywrapcp.DefaultRoutingSearchParameters()
	# Naive search: follow shortest arcs
	# search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
	# Better: Continue searching even after first optimum (which might be local)
	# If we use guided local search, we got to time limit the solution
	search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
	search_parameters.time_limit.seconds = 30

	# Solve it
	print("# Solving route (time limit:", search_parameters.time_limit.seconds, "seconds)")
	assignment = routing.SolveWithParameters(search_parameters)

	# Print optimized route
	if assignment:
		print("# Optimized route:")
		if(args.gmapjs):
			# Print solution that can be easily pasted into JavaScript calls for a Google Map
			print_solution_gmaps(manager, routing, assignment, data_model)
		else:
			# Print solution normally using arrows
			print_solution(manager, routing, assignment, data_model, True)
	else:
		print("# Oops, could not optimize route")

if __name__ == "__main__": main()
