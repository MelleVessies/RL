

from Codebase.collect_data import grid_search
from main import run_settings
import settings.cfg as cfg

if __name__ == '__main__':
    usable_environments = ['LunarLander-v2'"]
    grid_search(run_settings, cfg.no_tricks_settings, usable_environments, cfg.grid_search_range['eps_min'], cfg.grid_search_range['discount_factor'], cfg.training_seed_range, skip_completed=1)
