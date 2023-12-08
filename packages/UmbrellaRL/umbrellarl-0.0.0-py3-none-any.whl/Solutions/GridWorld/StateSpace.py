"""State Space for the Grid World."""

from typing import Tuple, List

from src.StateSpace import StateSpace

from Solutions.GridWorld.State import GridWorldState
from Solutions.GridWorld.Action import GridWorldAction

class GridWorldStateSpace(StateSpace[Tuple[int, int], GridWorldAction]):
    """Grid World State Space representation."""
    
    def __init__(self,
                 number_of_rows: int,
                 number_of_columns: int
                ) -> None:
        
        # TODO will probably have some config file for these terminal states. 
        terminal_states: List[Tuple[int, int]] = [(0, 0), (number_of_rows - 1, number_of_columns - 1)]
        
        self.number_of_rows = number_of_rows
        
        self.number_of_columns = number_of_columns
        
        for row in range(number_of_rows):
            
            for column in range(number_of_columns):
                
                grid_world_state: GridWorldState = GridWorldState(row, column)
                
                grid_world_state.actions = GridWorldAction.members()
                
                self[(row, column)] = grid_world_state
                
        for state in terminal_states:
            self[state].is_terminal = True
            self[state].reward = 1.0
                