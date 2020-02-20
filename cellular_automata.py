from backend import *
from matplotlib import pyplot as plt


def plot_lotka_volterra():
    '''

    :return:
    '''
    pred_br = 0.015
    pred_dr = 0.5
    prey_br = 0.5
    prey_dr = 0.1
    prey = [1000]
    predators = [0]
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


def plot_population_dynamics(time_array, prey, predators, title):
    plt.figure()
    plt.title(title)
    plt.plot(time_array, prey, color='b')
    plt.plot(time_array, predators, color='r')
    plt.xlabel("Generations")
    plt.ylabel("Prey(b) and Predator(r) Population")
    plt.show()


def plot_phase_portrait(predators, prey, title):
    plt.figure()
    plt.title(title)
    plt.plot(prey, predators)
    plt.xlabel("Prey Population")
    plt.ylabel("Predator Population")
    plt.show()


if __name__ == '__main__':
    #set parameters for system
    #format of param dict is: [prey_population, predator population, board size(n -> n-by-n board), prey birth rate,
    #prey death rate, predator birth rate, predator death rate, iterations of system(-1 for running until extinction)]
    param_dict = [[400,200,40,0.7,0.5,0.8,0.4,800]]#,[200,10,30,0.7,0.5,0.8,0.4, 150],[20,100,30,0.7,0.5,0.8,0.4, 150], [300, 10, 30, 0.5, 0.3, 0.7, 0.3, 300]]
    #param_dict = [[200, 100, 15, 0.5, 0.5, 0.9, 0.4, 500], [30, 30, 30, 0.5, 0.5, 0.9, 0.4, 500], [400, 200, 30, 0.5, 0.5, 0.9, 0.4, 500]]

    #param_dict = [[0, 100, 30, 0.7, 0.5, 0.8, 0.4, 20]]
    for param_list in param_dict:
        init_prey,init_predators, board_size, prey_brr, prey_drr, predator_br, predator_dr, iterations = param_list
        print(param_list)
        new_game = PPAC(n_rows=board_size, n_cols=board_size,initial_predators=init_predators,initial_prey=init_prey,predator_birth_rate=predator_br
                        ,predator_death_rate=predator_dr,prey_birth_rate=prey_brr, prey_death_rate=prey_drr, visuals_on=False)
        if iterations == -1:
            new_game.run()
        else:
            new_game.iterate(iterations)
        #information is saved in created object, use saved_data to view data, create graphs and plots, etc...
        data = [(i.Generation, i.NumberOfPrey, i.NumberOfPredators) for i in new_game.saved_data]
        time_stamps = [i[0] for i in data]
        prey_pop = [i[1] for i in data]
        pred_pop = [i[2] for i in data]
        plot_title = f"Population Dynamics:\nInitial Populations: Prey: {init_prey}, Predators: {init_predators}\n" +\
            f"Environment size: {board_size}-by-{board_size}\nRates: Prey Birth: {prey_brr} Death: {prey_drr} " +\
                f"Predator Birth: {predator_br} Death: {predator_dr}"
        plot_population_dynamics(time_stamps, prey_pop, pred_pop, plot_title)
        plot_phase_portrait(pred_pop, prey_pop, plot_title)
        #create plots based on LV equations to create comparison
    #plot_lotka_volterra()

