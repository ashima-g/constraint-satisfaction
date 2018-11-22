def solve_planes(planes_problem, algo, allsolns,
                 variableHeuristic='mrv', silent=False, trace=False):
    #Your implementation for Question 6 goes here.
    #
    #Do not but do not change the functions signature
    #(the autograder will twig out if you do).

    #If the silent parameter is set to True
    #you must ensure that you do not execute any print statements
    #in this function.
    #(else the output of the autograder will become confusing).
    #So if you have any debugging print statements make sure you
    #only execute them "if not silent". (The autograder will call
    #this function with silent=True, plane_scheduling.py will call
    #this function with silent=False)

    #You can optionally ignore the trace parameter
    #If you implemented tracing in your FC and GAC implementations
    #you can set this argument to True for debugging.
    #
    #Once you have implemented this function you should be able to
    #run plane_scheduling.py to solve the test problems (or the autograder).
    #
    #
    '''This function takes a planes_problem (an instance of PlaneProblem
       class) as input. It constructs a CSP, solves the CSP with bt_search
       (using the options passed to it), and then from the set of CSP
       solutions it constructs a list of lists specifying a schedule
       for each plane and returns that list of lists
       The required format is the list of lists is:

       For each plane P the list of lists contains a list L.
       L[0] == P (i.e., the first item of the list is the plane)
       and L[1], ..., L[k] (i.e., L[1:]) is the sequence of flights
       assigned to P.

       The returned list of lists should contain a list for every
       plane.
    '''

    #BUILD your CSP here and store it in the varable csp
    planes = []
    indices = {}
    k = 0
    for plane in planes_problem.planes:
    	vars = []
    	vars.append(plane)
    	for i in range(len(planes_problem.can_fly(plane))-1):
        	vars.append(Variable('{}{}'.format(plane, i), planes_problem.can_fly(plane)))
        	indices['{}{}'.format(plane,i)] = (k,i)
        planes.append(vars)
        k+=1
    
    cons = []
    allFlights = []
   
    for i in range(len(planes)): 
    	flights = planes[i]
    	currentPlane = flights[0]
    	flights.pop(0)
    	can_start = planes_problem.can_start(currentPlane)
    	can_start.pop(0) 
    	can_fly = planes_problem.can_fly(currentPlane)
    	can_fly.pop(0) 
    	
    	legal_start = set(can_fly).intersection(can_start)
    	K = planes_problem.min_maintenance_frequency
    	
    	cons.append(NValuesConstraint("first{}".format(currentPlane), flights[0:1], list(legal_start), 1, 1))
    	cons.append(NValuesConstraint("rest{}".format(currentPlane), flights[1:], can_fly, len(flights)-1, len(flights)-1))
    	
    	if K<=len(can_fly):
    		for j in range(len(can_fly)/K):
	    		cons.append(NValuesConstraint("maintenance{}".format(currentPlane), flights[((j*K)+j):((j+1)*K)], planes_problem.maintenance_flights, 1, len(flights)))
    	
    	scope = []
    	can_follow = planes_problem.can_follow
    	for k in range(len(can_follow)):
    		if (can_follow[k][0] in can_fly) and (can_follow[k][1] in can_fly):
    			scope.append(can_follow[k])		
    	
    	print ("trying this out", flights[2].getValue())
    	pairs = []
    	for j in range(len(flights)-1):
    		#combo = (flights[j],flights[j+1])
    		newVar = Variable('pair{}'.format(j),scope)
    		#newVar.setValue(combo)
    		
    		pairs.append(newVar)
    	
    	cons.append(NValuesConstraint("follow", pairs, scope, len(pairs), len(pairs)))
    		
    	allFlights.extend(flights)
	
	cons.append(AllDiffConstraint("flights", allFlights))
	
	allVars = []
	allVars.extend(allFlights)
	allVars.extend(pairs)
    
    csp = CSP("Planes", allVars, cons)
    #invoke search with the passed parameters
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)

    #Convert each solution into a list of lists specifying a schedule
    #for each plane in the format described above.
	
	#SOLUTIONS IS A LIST OF MUTILPLE VARIABLE ASSIGNMENTS --> FINSIH CONSTRAINT 4
	
    result = []
    
    for solution in solutions: 
    	for j in range(len(solution)):
    		print solution[j]
    		if 'pair' not in solution[j][0].name():
				index = indices[solution[j][0].name()]
				plane = index[0]
				flight = index[1] 
		
				planes[plane].insert(flight+1, solutions[j][1])
				planes[plane].pop(flight+2) # replace variable with values
				result.append(planes)			
	return result
	    

    #then return a list containing all converted solutions
    #(i.e., a list of lists of lists)
