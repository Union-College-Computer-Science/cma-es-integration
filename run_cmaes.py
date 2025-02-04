"""
Runs cma-es on `run_simulation.py` as a fitness function.
Continually updates output.csv with best individual from each generation.

Author: Thomas Breimer
February 4th, 2025
"""

import os
import sys
import pathlib
import run_simulation as sim
import CMA
import numpy as np
import pandas as pd

def run_cma_es(gens, sigma_val):
    """
    Runs the cma_es algorithm on the robot locomotion problem,
    with sin-like robot actuators. Saves a csv file to ./output
    with each robot's genome & fitness for every generation.

    Parameters:
        gens (int): How many generations to run.
        sigma_val (float): The standard deviation of the normal distribution
        used to generate new candidate solutions
    """

    # Generate Results DF
    df_cols = ['Generation', 'Individual', 'Fitness']

    for i in range(sim.NUM_ACTUATORS):
        df_cols = df_cols + ['frequency' + str(i), 'amplitude' + str(i),
                             'phase_offset' + str(i)]

    df = pd.DataFrame(columns=df_cols)

    optimizer = CMA(mean=np.array([sim.AVG_FREQ, sim.AVG_AMP, sim.AVG_PHASE_OFFSET] * sim.NUM_ACTUATORS),
                    sigma=sigma_val)

    for generation in range(gens):
        solutions = []

        for indv_num in range(optimizer.population_size):
            x = optimizer.ask()
            value = sim.run_simulation(sim.NUM_ITERS, x, False)
            solutions.append((x, value))
            to_add = [generation, indv_num, value] + list(x)
            df.loc[len(df)] = to_add


        optimizer.tell(solutions)
        print([i[1] for i in solutions])
        print("Generation", generation, "Best Fitness:", solutions[0][1])

    # Save csv
    this_dir = pathlib.Path(__file__).parent.resolve()
    df.to_csv(os.path.join(this_dir, 'output.csv'), index=False)


if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1:
        NUM_GENS = int(args[1])

    if len(args) > 2:
        SIGMA = float(args[2])

    run_cma_es(NUM_GENS, SIGMA)




