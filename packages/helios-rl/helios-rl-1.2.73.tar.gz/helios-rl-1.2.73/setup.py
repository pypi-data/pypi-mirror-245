from distutils.core import setup

setup(
    name='helios-rl',
    version='1.2.73',
    packages=[
        'helios_rl', 
        'helios_rl.adapters', 
        'helios_rl.agents',
        'helios_rl.benchmark',
        'helios_rl.encoders', 
        'helios_rl.environment_setup', 
        'helios_rl.evaluation',
        'helios_rl.reporting',
        'helios_rl.experiments',
        'helios_rl.interaction_loops',
        'helios_rl.hierarchies'
        ],
    # TODO: Add benchmark to exclusion of wheel
    url='https://github.com/pdfosborne/HELIOS-RL',
    license='GNU Public License v3',
    author='Philip Osborne',
    author_email='pdfosborne@gmail.com',
    description='Applying the HELIOS architecture to Reinforcement Learning problems.',
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy>=1.10.1',
        'torch',
        'sentence-transformers',
        'tqdm'
    ] 
)
