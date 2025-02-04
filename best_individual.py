import sys, pandas


ITERS = 200

"""
Look at output.csv and continuously run best individual.
Assumes csv names are their best achieved fitnesses
Continually searches for the lowest best fitness, plays the visualization and repeats
"""

def visualize_best(filename):

    df = pandas.read_csv("out/" + filename)

    try: #May need this in case file is currently being written to by run_cmaes

        best_fitness = min(df["Fitness"])
        row = df.loc[df['Fitness']==best_fitness]
        genome = row.values.tolist()[0][3:]
        #run_cma_es.run_simulation(ITERS, genome)

    except:
        visualize_best(filename)

    visualize_best(filename)
    


if __name__ == "__main__":

    args = sys.argv

    if len(args) < 2:
        print("Too few arguments!")
    else:
        visualize_best(str(args[1]))

    