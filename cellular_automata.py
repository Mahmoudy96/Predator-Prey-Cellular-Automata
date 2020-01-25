from backend import *
from matplotlib import pyplot as plt


def plot_lotka_volterra():
    pred_br = 0.015
    pred_dr = 0.5
    prey_br = 0.5
    prey_dr = 0.015
    prey = [100]
    predators = [10]
    # Defining the time frame
    delta_time = 0.01
    cycles = 4500

    # The model
    for t in range(0, cycles):
        updated_chickens = prey[t] + delta_time * (prey_br * prey[t]  - prey_dr * predators[t] * prey[t])
        updated_foxes = predators[t] + delta_time * (-pred_dr * predators[t] + pred_br * predators[t] * prey[t])
        prey.append(updated_chickens)
        predators.append(updated_foxes)

    # plotting
    time_points = range(cycles + 1)
    plt.figure()
    plt.plot(time_points, predators)
    plt.plot(time_points, prey)
    plt.xlabel('time')
    plt.show()


def plot_population_dynamics(time_array, prey, predators):
    plt.figure()
    plt.plot(time_stamps, prey_pop, color='b')
    plt.plot(time_stamps, pred_pop, color='r')
    plt.xlabel("Generations")
    plt.ylabel("Prey(b) and Predator(r) Population")
    plt.show()


def plot_phase_portrait(predators, prey):
    plt.figure()
    plt.plot(prey_pop, pred_pop)
    plt.xlabel("Prey Population")
    plt.ylabel("Predator Population")
    plt.show()


if __name__ == '__main__':
    #create desired game
    predator_br = 0.8
    predator_dr = 0.4
    prey_brr = 0.7
    prey_drr = 0.5
    init_prey = 200
    init_predators = 100
    new_game = PPAC(n_rows=40, n_cols=40,initial_predators=init_predators,initial_prey=init_prey,predator_birth_rate=predator_br
                    ,predator_death_rate=predator_dr,prey_birth_rate=prey_brr, prey_death_rate=prey_drr, visuals_on=True)
    #new_game.print_board()
    new_game.iterate(1000)
    print(new_game.saved_data, new_game.probabilities)
    #information is saved in created object, use saved_data to view data, create graphs and plots, etc...
    data = [(i.Generation, i.NumberOfPrey, i.NumberOfPredators) for i in new_game.saved_data]
    time_stamps = [i[0] for i in data]
    prey_pop = [i[1] for i in data]
    pred_pop = [i[2] for i in data]
    plot_population_dynamics(time_stamps, prey_pop, pred_pop)
    plot_phase_portrait(pred_pop, prey_pop)
    #create plots based on LV equations to create comparison
    plot_lotka_volterra()

#Define the rules
#Create the board, with a certain amount of predator and prey cells/nodes
    #Iterate the board according to the rules
    #Save the board state(number of predators/prey) for each step
#After a certain amount of times/steps or when the board is empty, plot the population dynamics
#Plot the population dynamics according to Lotka-Volterra equations with initial board parameters
#/(number of prey, number of predators, chance to reproduce/be eaten
#Compare CA plots to LV plots,

