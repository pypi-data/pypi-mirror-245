from datetime import datetime
import pandas as pd
import os
# ====== HELIOS IMPORTS =========================================
# ------ Train/Test Function Imports ----------------------------
from helios_rl import STANDARD_RL
from helios_rl import HELIOS_SEARCH
from helios_rl import HELIOS_OPTIMIZE
# ====== LOCAL IMPORTS ==========================================
# ------ Local Environment --------------------------------------
from helios_rl.benchmark.environment.sailing_env import Environment as Sailing
# ------ Benchmark Fixed Config -----------------------------------------------
# Meta parameters
from helios_rl.benchmark.benchmark_config import benchmark_config
# Local Parameters
from helios_rl.benchmark.benchmark_config_local import benchmark_local_config
# --------------------------------------------------------------------

# Specialised main run script to call standardised benchmark problems
# - Specify which problems that are to be used and evaluated on
# - Update and import the experiment dev setup 
def main(benchmark_settings:list=['sailing'], 
         num_train_epi:int=0, num_test_epi:int=0):
    """Train and testing experiments for the benchmark tests."""
    for benchmark in benchmark_settings:
        ExperimentConfig = benchmark_config[benchmark]
        ProblemConfig = benchmark_local_config[benchmark]
        # Specify save dir
        time = datetime.now().strftime("%d-%m-%Y_%H-%M")
        # Create output directory if it doesn't exist
        cwd = os.getcwd()
        if not os.path.exists(cwd+'/HELIOS-BENCHMARK-output'):
            os.mkdir(cwd+'/HELIOS-BENCHMARK-output')
        save_dir = cwd+'/HELIOS-BENCHMARK-output/'+str('test')+'_'+time 

        if num_train_epi != 0:
            ExperimentConfig['number_training_episodes'] = num_train_epi
        if num_test_epi != 0:
            ExperimentConfig['number_test_episodes'] = num_test_epi
        
        # --------------------------------------------------------------------
        # EXPERIMENTS TO DEVELOP
        # --------------------------------------------------------------------
        # # HELIOS Instruction Following
        # num_plans = 50
        # num_explor_epi = 1000
        # sim_threshold = 0.9

        # observed_states = None
        # instruction_results = None
        
        # helios = HELIOS_SEARCH(Config=ExperimentConfig, LocalConfig=ProblemConfig, 
        #                     Environment=Sailing,
        #                     save_dir = save_dir+'/Reinforced_Instr_Experiment',
        #                     num_plans = num_plans, number_exploration_episodes=num_explor_epi, sim_threshold=sim_threshold,
        #                     feedback_increment = 0.1, feedback_repeats=1,
        #                     observed_states=observed_states, instruction_results=instruction_results)

        # # Don't provide any instruction information, will be defined by command line input
        # helios_results = helios.search(action_cap=100, re_search_override=False, simulated_instr_goal=None)

        # # Store info for next plan -> assumes we wont see the same instruction twice in one plan
        # observed_states = helios_results[0]
        # instruction_results = helios_results[1]
        # # --------------------------------------------------------------------
        # # Take Instruction path now defined with reinforced+unsupervised sub-goal locations and train to these
        # # Init experiment setup with sub-goal defined
        # reinforced_experiment = HELIOS_OPTIMIZE(Config=ExperimentConfig, LocalConfig=ProblemConfig, 
        #                 Environment=Sailing,
        #                 save_dir=save_dir+'/Reinforced_Instr_Experiment', show_figures = 'No', window_size=0.1,
        #                 instruction_path=None, predicted_path=instruction_results, instruction_episode_ratio=0.05,
        #                 instruction_chain=True, instruction_chain_how='exact' )
        # reinforced_experiment.train()
        # reinforced_experiment.test()
        # --------------------------------------------------------------------
        # Flat Baselines
        flat = STANDARD_RL(Config=ExperimentConfig, LocalConfig=ProblemConfig, 
                    Environment=Sailing,
                    save_dir=save_dir, show_figures = 'No', window_size=0.1)
        flat.train()  
        flat.test()
        # --------------------------------------------------------------------

def run_benchmark():
    possible_benchmarks = ['sailing']
    benchmark_list = []
    while True:
        benchmark = input('Enter benchmark to run from '+ str(possible_benchmarks)+ ' (hit enter to continue): ')
        if benchmark == '':
            break
        elif benchmark not in possible_benchmarks:
            print('Invalid benchmark, please try again.')
        else:
            benchmark_list.append(benchmark)
    print("Please enter the number of ... (skip to use default) ")
    num_train_epi = int(input('\t - Training episodes: '))
    num_test_epi = int(input('\t - Testing episodes: '))
    if num_train_epi == '':
        num_train_epi = 0
    if num_test_epi == '':
        num_test_epi = 0
    main(benchmark_settings=benchmark_list, num_train_epi=num_train_epi, num_test_epi=num_test_epi)

if __name__=='__main__':
    run_benchmark()