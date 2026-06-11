# AI Creatures

AI Creatures is a Python project that simulates the evolution of simple virtual creatures in a physics environment.

The project uses a genetic algorithm to generate creature bodies and movement patterns. Each creature is represented by a genome, converted into a URDF robot model, loaded into PyBullet, and evaluated based on how far it can move.

## Project Overview

The goal of this project is to explore artificial evolution through physics-based simulation.

A population of random creatures is created, simulated, scored, and evolved over multiple generations. Better-performing creatures are more likely to be selected as parents for the next generation.

The project demonstrates concepts from:

- Genetic algorithms
- Procedural creature generation
- Physics simulation
- Evolutionary robotics
- URDF-based robot modelling

## How It Works

The basic workflow is:

1. Generate a population of random creatures.
2. Encode each creature using a genome.
3. Convert the genome into a physical creature body.
4. Export the creature as a URDF model.
5. Load the model into PyBullet.
6. Simulate movement using simple motor controllers.
7. Measure the distance travelled by each creature.
8. Select better-performing creatures.
9. Apply crossover and mutation.
10. Repeat the process over many generations.

## Repository Structure

```text
AI-creatures/
├── creature.py             # Creature class, body generation, motors, fitness tracking
├── genome.py               # Genome encoding, mutation, crossover, URDF link generation
├── population.py           # Population management and parent selection
├── simulation.py           # PyBullet simulation logic
├── starter.py              # Starter script / example entry point
├── motor_test.py           # Motor behaviour testing
├── offline_sim_test.py     # Offline simulation test
├── test_creature.py        # Creature unit tests
├── test_genome.py          # Genome unit tests
├── test_population.py      # Population unit tests
├── test_simulation.py      # Simulation unit tests
├── test_ga.py              # Genetic algorithm test
├── test.urdf               # Example URDF file
├── 103.urdf                # Example/generated creature URDF
└── README.md
```

## Main Components

### Genome

The genome stores the information needed to build and control a creature.

It defines properties such as:

- body segment length
- body segment radius
- mass
- parent-child link relationships
- joint position
- joint axis
- motor waveform
- motor amplitude
- motor frequency

The genome also supports evolutionary operations such as:

- crossover
- point mutation
- grow mutation
- shrink mutation

### Creature

A creature is built from a genome.

The creature class is responsible for:

- generating a random genome
- expanding genes into body links
- creating motor controllers
- producing URDF XML
- tracking starting and ending positions
- calculating fitness based on distance travelled

### Simulation

The simulation uses PyBullet to evaluate each creature.

During simulation:

- the environment is reset
- a floor plane is created
- the creature URDF is loaded
- motors are applied to joints
- the physics world is stepped forward
- the creature's movement is measured

### Population

The population module manages groups of creatures.

It provides logic for selecting parents based on fitness, so creatures that move farther are more likely to pass their genomes to the next generation.

## Installation

Clone the repository:

```bash
git clone https://github.com/rmwua/AI-creatures.git
cd AI-creatures
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install pybullet numpy
```

If you want to run the tests:

```bash
pip install pytest
```

## Usage

Run the genetic algorithm test:

```bash
python test_ga.py
```

Run a simulation test:

```bash
python test_simulation.py
```

Run all tests:

```bash
pytest
```

## Example Evolution Loop

A simplified version of the process looks like this:

```python
from population import Population
from simulation import Simulation

population = Population(pop_size=10, gene_count=3)
simulation = Simulation()

for generation in range(100):
    for creature in population.creatures:
        simulation.run_creature(creature, 2400)

    fits = [creature.get_distance_travelled() for creature in population.creatures]
    print(f"Generation {generation}: best fitness = {max(fits)}")
```

## Fitness Function

The current fitness function is based on distance travelled.

A creature starts at an initial position in the physics world. After simulation, the distance between its starting position and final position is calculated. Creatures that travel farther receive higher fitness scores.

## Technologies Used

- Python
- PyBullet
- NumPy
- URDF
- Pytest


