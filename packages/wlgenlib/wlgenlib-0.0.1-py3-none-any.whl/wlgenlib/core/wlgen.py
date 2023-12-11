import simpy
import numpy as np
from pathlib import Path
from loguru import logger
from omegaconf import OmegaConf
from wlgen.core.tasks import Tasks
from wlgen.core.blocks import Blocks
from wlgen.core.resourcemanager import ResourceManager

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_CONFIG_FILE = REPO_ROOT.joinpath("config/config.json")


class WLGen:
    def __init__(self, omegaconf, dp_engine_hook, task_generator, block_generator):
        self.env = simpy.Environment()

        # Initialize configuration
        default_config = OmegaConf.load(DEFAULT_CONFIG_FILE)
        omegaconf = OmegaConf.create(OmegaConf.load(omegaconf))
        self.config = OmegaConf.merge(default_config, omegaconf)
        print(omegaconf)
        logger.info(f"Configuration: {self.config}")

        rng = (
            np.random.default_rng()
            if self.config.enable_random_seed
            else np.random.default_rng(self.config.global_seed)
        )

        # Start the block and tasks consumers
        self.rm = ResourceManager(
            self.env, dp_engine_hook, task_generator, block_generator, self.config
        )
        self.env.process(self.rm.start())

        # Start the block and tasks producers
        Blocks(self.env, self.rm)
        Tasks(self.env, self.rm, rng)

    def run(self):
        self.env.run()
