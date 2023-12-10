import torch
from evotorch import Problem
from evotorch.operators import SimulatedBinaryCrossOver, GaussianMutation
from evotorch.logging import StdOutLogger
import torch.nn as nn
from collections.abc import Iterable

from src.geneticAlgorithms import SteadyStateGAWithEarlyStopping
from src.neuralNetworkEstimator import NeuralNetwork

def get_last_layer_shape(model):
    for layer in reversed(list(model.modules())):
            return layer.weight.shape, layer.weight
    return None

def set_layer_weights(model, layer_index, new_weights):
    i = 0
    for layer in reversed(list(model.modules())):
                layer.weight.data = new_weights
                return
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')
set_layer_weights(model, 0, torch.Tensor([0 for i in range(768)]))
print(get_last_layer_shape(model))
class HuggingFaceFunction:
    """
    Class to handle genetic optimization for a given problem, using objective functions.
    This class is designed to be agnostic of the specific details of the problem being optimized.
    """

    def __init__(self, modelName, numberOfLayers):
        """
        Initializes the genetic optimization class with a neural network model.

        :param input_shape: Integer, the size of the input layer of the neural network.
        :param output_shape: Integer, the size of the output layer of the neural network.
        """
        model = GPT2Model.from_pretrained('gpt2')
        self.shape,self.weights = get_last_layer_shape(model)
        self.input_shape = self.shape[0]
        self.model = model
        self.solution_length = self.model.get_solution_length()
        self.objectives = []
        self.maximizeOrMinimize = []

    def infer(self ,input_data ,weights=None):
        """
        Performs inference using the model with the given weights on the input data.

        :param input_data: The data on which inference is to be performed.
        :param weights: The weights to be set in the neural network model for inference.
        :return: The output of the model after performing inference.
        """
        # Set the provided weights to the model
        if weights is not None:
            self.model.set_weights(weights.clone())
        # Perform inference
        output = self.model.model(input_data)

        return output

    def set_weights(self,weights):
        if weights is not None:
            self.model.set_weights(weights.clone())

    def add_objective(self, objective_func, maximize=False, size=1):
        """
        Adds an objective function to the optimization process.

        :param objective_func: A callable that takes the model as an argument and returns a fitness score.
        """
        self.objectives.append(objective_func)
        if maximize:
            for i in range(size):
                self.maximizeOrMinimize.append("max")
        else:
            for i in range(size):
                self.maximizeOrMinimize.append("min")



    def evaluate_fitness(self, weights: torch.Tensor):
        """
        Evaluate the fitness of a solution based on the added objective functions.

        :param weights: Torch tensor, the weights to be set in the neural network model for evaluation.
        :return: Torch tensor, the computed fitness scores.
        """
        fitness_scores = [[] for o in self.maximizeOrMinimize]
        for x in weights:
            self.model.set_weights(x.clone())
            i=0
            for objective in self.objectives:
                score = objective(self.model)
                if isinstance(score, Iterable)and len(score)>1:
                    for s in score:
                        fitness_scores[i].append(s)
                        i += 1
                else:
                    fitness_scores[i].append(score)
                    i+=1
        if len(fitness_scores)>0:
            return   torch.stack([torch.tensor(f) for f in fitness_scores], dim=-1)
        else:
            return None

    def get_solution_length(self):
        """
        Returns the solution length of the neural network model.
        """
        return self.model.get_solution_length()

    def optimize(self, population_size=200, num_generations=100, tournament_size=2,cross_over_rate=0.95,eta=1,stdev=0.1):
        """
        Runs the genetic algorithm optimization.

        :param population_size: Integer, the size of the population for the genetic algorithm.
        :param num_generations: Integer, the number of generations for the genetic algorithm to run.
        """
        # Define the problem for the genetic algorithm
        problem = Problem(
            self.maximizeOrMinimize,  # Define the direction of optimization (minimization in this case)
            self.evaluate_fitness,             # Fitness evaluation function
            initial_bounds=(-1.0, 1.0),        # Initial bounds for the solutions
            solution_length=self.solution_length,
            vectorized=True
        )

        # Initialize the genetic algorithm
        ga = SteadyStateGAWithEarlyStopping(problem ,popsize=population_size)

        # Works like NSGA-II for multiple objectives
        ga.use(
            SimulatedBinaryCrossOver(problem ,tournament_size=tournament_size ,cross_over_rate=cross_over_rate ,
                                     eta=eta))
        ga.use(GaussianMutation(problem ,stdev=stdev))
        logger = StdOutLogger(ga)
        best ,steps = ga.run(num_generations,self.evaluate_fitness)
        resultingWeights = ga.population.values
        fitnesses = self.evaluate_fitness(resultingWeights)
        return ga.weights,ga.fitnesses




from transformers import GPT2Tokenizer, GPT2Model
import torch
from transformers import Trainer, TrainingArguments
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(10, 20)  # First linear layer
        self.fc2 = nn.Linear(20, 30)  # Second linear layer
        self.fc3 = nn.Linear(30, 40)  # Last linear layer

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Create an instance of the model
model = SimpleNN()
def get_last_layer_shape(model):
    for layer in reversed(list(model.modules())):
            return layer.weight.shape, layer.weight
    return None

def set_layer_weights(model, layer_index, new_weights):
    i = 0
    for layer in reversed(list(model.modules())):
                layer.weight.data = new_weights
                return
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')
set_layer_weights(model, 0, torch.Tensor([0 for i in range(768)]))
print(get_last_layer_shape(model))
#text = "Replace me by any text you'd like."
#encoded_input = tokenizer(text, return_tensors='pt')
#output = model(**encoded_input)