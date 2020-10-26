

from Codebase.collect_data import grid_search2
from main import run_settings
import settings.cfg as cfg

if __name__ == '__main__':
    usable_environments = ["'CartPole-v1'"]
    grid_search2(run_settings, cfg.no_tricks_settings, usable_environments, cfg.tuple_search, cfg.training_seed_range, skip_completed=0)
