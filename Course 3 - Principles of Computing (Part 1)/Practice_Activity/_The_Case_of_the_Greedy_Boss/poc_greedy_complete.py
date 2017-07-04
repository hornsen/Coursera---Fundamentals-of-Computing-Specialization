"""
Simulator for greedy boss scenario
"""

#import simpleplot
import pylab
import matplotlib.pyplot as plt

import math


STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type = STANDARD):
    """
    Simulation of greedy boss
    """

    # initialize necessary local variables
    current_day = 0
    total_salary = 0
    total_bribe = 0
    bribe = 0

    # define  list consisting of days vs. total salary earned for analysis
    days_vs_earnings = [(0, 0)]

    # Each iteration of this while loop simulates one bribe
    while current_day < days_in_simulation:
        day_counter=0

        while True:
            # update list with days vs total salary earned
            # use plot_type to control whether regular or log/log plot
            day_counter+=1
            total_salary_temp = day_counter * ( INITIAL_SALARY + (SALARY_INCREMENT * bribe) )
            total_bribe_temp = INITIAL_BRIBE_COST + bribe_cost_increment * bribe
            
            # check whether we have enough money to bribe without waiting    
            if( total_salary + total_salary_temp >= total_bribe + total_bribe_temp ):
                
                # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY)
                total_salary += total_salary_temp
                total_bribe += total_bribe_temp
                current_day += day_counter
                bribe += 1

                # update state of simulation to reflect bribe
                days_vs_earnings.append((current_day, total_salary))

                break

    return days_vs_earnings


def run_simulations():
    """
    Run simulations for several possible bribe increments
    """
    plot_type = STANDARD
    days = 70
    inc_0 = greedy_boss(days, 0, plot_type)
    inc_500 = greedy_boss(days, 500, plot_type)
    inc_1000 = greedy_boss(days, 1000, plot_type)
    inc_2000 = greedy_boss(days, 2000, plot_type)

    plt.plot( inc_0 )
    plt.plot( inc_500 )
    plt.plot( inc_1000 )
    plt.plot( inc_2000 )
    
    plt.legend(['inc_0', 'inc_500', 'inc_1000', 'inc_2000'], loc='upper left')

    plt.show()

run_simulations()

print greedy_boss(35, 100)
# should print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700)]

print greedy_boss(35, 0)
# should print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (35, 16800)]



print("")
print(greedy_boss(35, 100) == [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700)])
print(greedy_boss(35, 0) == [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (35, 16800)])
