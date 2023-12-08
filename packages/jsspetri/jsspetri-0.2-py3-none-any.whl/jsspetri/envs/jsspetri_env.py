import numpy as np
from gymnasium import Env
from gymnasium import spaces

from jsspetri.envs.simulator import JSSPSimulator
from jsspetri.render.gui import Gui
from jsspetri.render.solution_plot import plot_solution
from jsspetri.render.create_directory import create_new_directory

class JsspetriEnv(Env):
    """
    Custom Gym environment for Job Shop Scheduling using a Petri net simulator.
    """
    metadata = {"render_modes": ["human", "solution"]}

    def __init__(self, render_mode=None, instance_id="ta01", observation_depth=1):
        """
        Initializes the JsspetriEnv.

        Parameters:
            render_mode (str): Rendering mode ("human" or "solution").
            instance_id (str): Identifier for the JSSP instance.
            observation_depth (int): Depth of observations for each job.
        """
        self.sim = JSSPSimulator(instance_id)
        self.observation_depth = min(observation_depth, self.sim.n_machines)
        self.observation_space = spaces.Box(low=-1, high=self.sim.max_bound,
                                            shape=(2 * self.sim.n_machines + 2 * (self.sim.n_jobs * self.observation_depth) + self.sim.n_machines,),
                                            dtype=np.int64)
        self.action_space = spaces.Discrete(self.sim.n_machines * self.sim.n_jobs + 1)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        if render_mode is None:
            self.gui = None
        else:
            self.gui = Gui(self.sim)
            self.gui.render_mode = render_mode
            create_new_directory(self.sim, self.gui)

    def _get_obs(self):
        """
        Get the observation state.

        Returns:
            np.ndarray: Observation array.
        """
        observation = []
        job_places = [p for p in self.sim.places.values() if p.uid in self.sim.filter_nodes("job")]
        machine_places = [p for p in self.sim.places.values() if p.uid in self.sim.filter_nodes("machine")]
        finished_places = [p for p in self.sim.places.values() if p.uid in self.sim.filter_nodes("finished_ops")]

        # Get the state of the machines, i.e., remaining time if not idle:
        for machine in machine_places:
            if len(machine.token_container) == 0:
                observation.extend([machine.color, -1])
            else:
                in_process = machine.token_container[0]
                remaining_time = in_process.process_time - in_process.logging[list(in_process.logging.keys())[-1]][2]
                observation.extend([machine.color, remaining_time if remaining_time >= 0 else -1])

        # Get the waiting operation in the jobs depending on the depth:
        for level in range(self.observation_depth):
            for job in job_places:
                if job.token_container and level < len(job.token_container):
                    observation.extend([job.token_container[level].color[1], job.token_container[level].process_time])
                else:
                    observation.extend([-1, -1])

        # Get the number of delivered operations
        for delivery in finished_places:
            observation.append(len(delivery.token_container))

        return np.array(observation, dtype=np.int64)

    def reset(self, seed=None, options=None):
        """
        Reset the environment.

        Returns:
            tuple: Initial observation and info.
        """
        self.sim.petri_reset()
        observation = self._get_obs()
        info = self._get_info(0, False)

        return observation, info

    def reward(self, advantage):
        """
        Calculate the reward.

        Parameters:
            fired (bool): Whether a transition was fired.
            advantage: Advantage information.

        Returns:
            Any: Calculated reward.
        """
        return advantage

    def action_masks(self):
        """
        Get the action masks.

        Returns:
            list: List of enabled actions.
        """
        enabled_mask = self.sim.enabled_allocations()
        return enabled_mask

    def step(self, action):
        """
        Take a step in the environment.

        Parameters:
            action: Action to be performed.

        Returns:
            tuple: New observation, reward, termination status, info.
        """
        fired, advantage = self.sim.petri_interact(self.gui, action)
        reward = self.reward(advantage)
        observation = self._get_obs()
        terminated = self.sim.is_terminal()
        info = self._get_info(reward, terminated)

        return observation, reward, terminated, False, info

    def render(self):
        """
        Render the environment.
        """
        if self.gui.render_mode == "solution":
            plot_solution(self.sim, self.gui)
        elif self.gui.render_mode == "human":
            plot_solution(self.sim, self.gui)
            self.gui.launch_gui()

    def close(self):
        """
        Close the environment.
        """
        if self.metadata["render_modes"] == "human":
            self.gui.on_window_close()

    def _get_info(self, reward, terminated):
        """
        Get information dictionary.

        Parameters:
            reward: Current reward.
            terminated (bool): Termination status.

        Returns:
            dict: Information dictionary.
        """
        return {"Reward": reward, "Terminated": terminated}

if __name__ == "__main__":
    pass
