import random

def time_val(time):
    value = 0
    # Return an integer value for the entered time. This value is used to determine proxity to another time.
    if time == "10 AM":
        value = 0
    elif time == "11 AM":
        value = 1
    elif time == "12 PM":
        value = 2
    elif time == "1 PM":
        value = 3
    elif time == "2 PM":
        value = 4
    elif time == "3 PM":
        value = 5
    return value

def room_capacity(room):
    value = 0
    # Return the room capacity for the entered room
    if room == "Slater 003":
        value = 45
    elif room == "Roman 216":
        value = 30
    elif room == "Loft 206":
        value = 75
    elif room == "Roman 201":
        value = 50
    elif room == "Loft 310":
        value = 108
    elif room == "Beach 201":
        value = 60
    elif room == "Beach 301":
        value = 75
    elif room == "Logos 325":
        value = 450
    elif room == "Frank 119":
        value = 60
    return value

def enrollment(act):
    value = 0
    # return the expected enrollment size for the entered activity
    if act == "SLA101A":
        value = 50
    elif act == "SLA101B":
        value = 50
    elif act == "SLA191A":
        value = 50
    elif act == "SLA191B":
        value = 50
    elif act == "SLA201":
        value = 50
    elif act == "SLA291":
        value = 50
    elif act == "SLA303":
        value = 60
    elif act == "SLA304":
        value = 25
    elif act == "SLA394":
        value = 20
    elif act == "SLA449":
        value = 60
    elif act == "SLA451":
        value = 100
    return value

def preferred_facs(act):
    facs = []
    # return an array of preferred facilitators for the entered activity
    if act == "SLA101A":
        facs = ["Glen", "Lock", "Banks", "Zeldin"]
    elif act == "SLA101B":
        facs = ["Glen", "Lock", "Banks", "Zeldin"]
    elif act == "SLA191A":
        facs = ["Glen", "Lock", "Banks", "Zeldin"]
    elif act == "SLA191B":
        facs = ["Glen", "Lock", "Banks", "Zeldin"]
    elif act == "SLA201":
        facs = ["Glen", "Shaw", "Banks", "Zeldin"]
    elif act == "SLA291":
        facs = ["Singer", "Lock", "Banks", "Zeldin"]
    elif act == "SLA303":
        facs = ["Glen", "Banks", "Zeldin"]
    elif act == "SLA304":
        facs = ["Glen", "Banks", "Tyler"]
    elif act == "SLA394":
        facs = ["Tyler", "Singer"]
    elif act == "SLA449":
        facs = ["Tyler", "Singer", "Shaw"]
    elif act == "SLA451":
        facs = ["Tyler", "Singer", "Shaw"]
    return facs

def other_facs(act):
    facs = []
    # return an array of other facilitators for the entered activity
    if act == "SLA101A":
        facs = ["Numen", "Richards"]
    elif act == "SLA101B":
        facs = ["Numen", "Richards"]
    elif act == "SLA191A":
        facs = ["Numen", "Richards"]
    elif act == "SLA191B":
        facs = ["Numen", "Richards"]
    elif act == "SLA201":
        facs = ["Numen", "Richards", "Singer"]
    elif act == "SLA291":
        facs = ["Numen", "Richards", "Shaw", "Tyler"]
    elif act == "SLA303":
        facs = ["Numen", "Singer", "Shaw"]
    elif act == "SLA304":
        facs = ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"]
    elif act == "SLA394":
        facs = ["Richards", "Zeldin"]
    elif act == "SLA449":
        facs = ["Zeldin", "Uther"]
    elif act == "SLA451":
        facs = ["Zeldin", "Uther", "Richards", "Banks"]
    return facs

def fitness_function(state):
    score = 0.00 # fitness score for whole schedule
    gene = 0
    
    while gene < 11: # iterate through all 11 activities in a schedule
        fitness = 0.00 # activity fitness score

        time = time_val(state[gene][2])
        capacity = room_capacity(state[gene][1])
        size = enrollment(state[gene][0])
        preferred = preferred_facs(state[gene][0])
        other = other_facs(state[gene][0])

        # checks if activity is scheduled at the same time and room as another
        i = 0
        sub = False
        while i < 11:
            if state[gene][1] == state[i][1] and state[gene][2] == state[i][2] and gene != i:
                sub = True
            i += 1
        if sub == True:
            fitness -= 0.50

        # checks if room is too small, three times the capacity, or six times the capacity
        if capacity < size:
            fitness -= 0.50
        elif capacity > (size * 6):
            fitness -= 0.40
        elif capacity > (size * 3):
            fitness -= 0.20
        else:
            fitness += 0.30

        # checks if the activity has a preferred or other facilitator
        if state[gene][3] in preferred:
            fitness += 0.50
        elif state[gene][3] in other:
            fitness += 0.20
        else:
            fitness -= 0.10

        # checks if facilitator is scheduled for another activity at the same time
        i = 0
        sub = False
        while i < 11:
            if state[gene][3] == state[i][3] and state[gene][2] == state[i][2] and gene != i:
                sub = True
            i += 1
        if sub == True:
            fitness -= 0.20
        if sub == False:
            fitness += 0.20

        # checks if facilitator has more than 4 activities or less than 3 activities schedules
        i = 0
        act_load = 0
        while i < 11:
            if state[gene][3] == state[i][3]:
                act_load += 1
            i += 1
        if act_load > 4:
            fitness -= 0.50
        elif act_load < 3 and state[gene][3] != "Tyler":
            fitness -= 0.40

        # checks to see if facilitator has consecutive timeslots and if they are both in Roman or Beach rooms
        romans = ["Roman 216", "Roman 201"]
        beachs = ["Beach 201", "Beach 301"]
        i = 0
        sub = False
        ad = False
        while i < 11:
            time2 = time_val(state[i][2])
            if abs(time - time2) == 1 and state[gene][3] == state[i][3]:
                if (state[gene][1] in romans and state[i][1] not in romans) or (state[gene][1] in beachs and state[i][1] not in beachs) or (state[i][1] in beachs and state[gene][1] not in beachs) or (state[i][1] in romans and state[gene][1] not in romans):
                    sub = True
                else:
                    ad = True
            i += 1
        if sub == True:
            fitness -= 0.40
        if ad == True:
            fitness += 0.50

        # checks if activity is a section of SLA 101 or 191 and if it is 4 hours apart or at the same time as another section of SLA 101 or 191
        sla101 = ["SLA101A", "SLA101B"]
        sla191 = ["SLA191A", "SLA191B"]
        if state[gene][0] in sla101:
            i = 0
            while i < 11:
                time2 = time_val(state[i][2])
                if abs(time - time2) > 4 and state[i][0] in sla101:
                    fitness += 0.50
                elif abs(time - time2) == 0 and state[i][0] in sla101 and gene != i:
                    fitness -= 0.50
                i += 1
        if state[gene][0] in sla191:
            i = 0
            while i < 11:
                time2 = time_val(state[i][2])
                if abs(time - time2) > 4 and state[i][0] in sla191:
                    fitness += 0.50
                elif abs(time - time2) == 0 and state[i][0] in sla191 and gene != i:
                    fitness -= 0.50
                i += 1

        # checks if a section of SLA 191 and SLA 101 are in consecutive slots and if they are both in Roman or Beach rooms
        i = 0
        sub = False
        ad = False
        while i < 11:
            time2 = time_val(state[i][2])
            if (abs(time - time2) == 1 and state[gene][0] in sla101 and state[i][0] in sla191) or (abs(time - time2) == 1 and state[gene][0] in sla191 and state[i][0] in sla101):
                if (state[gene][1] in romans and state[i][1] not in romans) or (state[gene][1] in beachs and state[i][1] not in beachs) or (state[i][1] in beachs and state[gene][1] not in beachs) or (state[i][1] in romans and state[gene][1] not in romans):
                    sub = True
                else:
                    ad = True
            i += 1
        if sub == True:
            fitness -= 0.40
        if ad == True:
            fitness += 0.50

        # check if a section of SLA 191 and SLA 101 are separated by an hour or in the same time slot
        i = 0
        ad = False
        sub = False
        while i < 11:
            time2 = time_val(state[i][2])
            if (abs(time - time2) == 2 and state[gene][0] in sla101 and state[i][0] in sla191) or (abs(time - time2) == 2 and state[gene][0] in sla191 and state[i][0] in sla101):
                ad = True
            elif (abs(time - time2) == 0 and state[gene][0] in sla101 and state[i][0] in sla191) or (abs(time - time2) == 0 and state[gene][0] in sla191 and state[i][0] in sla101):
                sub = True
            i += 1
        if ad == True:
            fitness += 0.25
        if sub == True:
            fitness -= 0.25

        score += fitness
        gene += 1
        
    return score

def randomize_activity(act):
    # makes three random integers, one for chosing a room, one for chosing a time, and one for chosing a facilitator for the activity
    rand1 = random.randint(0, 8)
    rand2 = random.randint(0, 5)
    rand3 = random.randint(0, 9)

    rooms = ["Slater 003", "Roman 216", "Loft 206", "Roman 201", "Loft 310", "Beach 201", "Beach 301", "Logos 325", "Frank 119"]
    times = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]
    facs = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]

    room = rooms[rand1]
    time = times[rand2]
    facilitator = facs[rand3]
    
    activity = [act, room, time, facilitator]
    return activity

def randomize_state():
    # calls the randomize_activity function for all 11 activities in a schedule
    state = []
    act = "SLA101A"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA101B"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA191A"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA191B"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA201"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA291"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA303"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA304"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA394"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA449"
    activity = randomize_activity(act)
    state.append(activity)
    act = "SLA451"
    activity = randomize_activity(act)
    state.append(activity)
    return state

def randomize_population(population_size):
    population = []
    # iterate through population size and add a number of randomized schedules to the population equal to that size
    while population_size > 0:
        population_size -= 1
        state = randomize_state()
        population.append(state)
    return population

def genetic_algorithm(population, mutation_rate, num_generations):
    population_size = len(population)
    num_parents = population_size // 2
    num_genes = len(population[0])
    generation = 0
    current_mutation_rate = mutation_rate
    
    for i in range(num_generations):
        # calculate fitness scores for each state in the population
        fitness_scores = [fitness_function(state) for state in population]

        # Check if the best fitness score improved from the previous generation's best score and decrease mutation rate by half if so
        curr_fitness = max(fitness_scores)
        if generation > 0 and curr_fitness > prev_fitness:
            current_mutation_rate /= 2.0
        prev_fitness = curr_fitness
        
        # select parents based on fitness scores
        parents = [population[i] for i in sorted(range(population_size), key=lambda x: fitness_scores[x], reverse=True)[:num_parents]]
        
        # create offspring by crossover and mutation
        offspring = []
        for j in range(num_parents):
            parent1 = parents[j]
            parent2 = random.choice(parents)
            child = []
            for k in range(num_genes):
                if random.random() < current_mutation_rate:
                    mutant_state = randomize_state()
                    child.append(mutant_state)
                else:
                    if random.random() < 0.5:
                        child.append(parent1[k])
                    else:
                        child.append(parent2[k])
            offspring.append(child)
        
        # replace the least fit half of the population with the offspring
        population = sorted(population, key=lambda x: fitness_function(x))
        population[:population_size//2] = offspring
        generation += 1
        
    # calculate fitness scores for the final population
    fitness_scores = [fitness_function(state) for state in population]
    
    # find the best state and its fitness score
    best_state = population[fitness_scores.index(max(fitness_scores))]
    best_fitness = max(fitness_scores)
    
    return best_state, best_fitness

if __name__ == '__main__':
    population = randomize_population(500) # creates randomized first generation with population size of 500
    final_state, final_fitness = genetic_algorithm(population, 0.01, 100) # calls genetic algorithm with the initial population, an initial mutation rate of .01, and 100 generations to run
    with open("output.txt", 'a') as file:
        # Prints the best fitness score and schedule from the last generation to an output text file
        line = f'\nBest fitness score from final generation: {final_fitness}\n'
        file.write(line)
        line = f'Activity: SLA100A   Rooom: {final_state[0][1]}   Time: {final_state[0][2]}   Facilitator: {final_state[0][3]}\n'
        file.write(line)
        line = f'Activity: SLA100B   Rooom: {final_state[1][1]}   Time: {final_state[1][2]}   Facilitator: {final_state[1][3]}\n'
        file.write(line)
        line = f'Activity: SLA191A   Rooom: {final_state[2][1]}   Time: {final_state[2][2]}   Facilitator: {final_state[2][3]}\n'
        file.write(line)
        line = f'Activity: SLA191B   Rooom: {final_state[3][1]}   Time: {final_state[3][2]}   Facilitator: {final_state[3][3]}\n'
        file.write(line)
        line = f'Activity: SLA201   Rooom: {final_state[4][1]}   Time: {final_state[4][2]}   Facilitator: {final_state[4][3]}\n'
        file.write(line)
        line = f'Activity: SLA291   Rooom: {final_state[5][1]}   Time: {final_state[5][2]}   Facilitator: {final_state[5][3]}\n'
        file.write(line)
        line = f'Activity: SLA303   Rooom: {final_state[6][1]}   Time: {final_state[6][2]}   Facilitator: {final_state[6][3]}\n'
        file.write(line)
        line = f'Activity: SLA304   Rooom: {final_state[7][1]}   Time: {final_state[7][2]}   Facilitator: {final_state[7][3]}\n'
        file.write(line)
        line = f'Activity: SLA394   Rooom: {final_state[8][1]}   Time: {final_state[8][2]}   Facilitator: {final_state[8][3]}\n'
        file.write(line)
        line = f'Activity: SLA449   Rooom: {final_state[9][1]}   Time: {final_state[9][2]}   Facilitator: {final_state[9][3]}\n'
        file.write(line)
        line = f'Activity: SLA451   Rooom: {final_state[10][1]}   Time: {final_state[10][2]}   Facilitator: {final_state[10][3]}\n'
        file.write(line)
    
