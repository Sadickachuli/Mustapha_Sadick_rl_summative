# main.py
import argparse
import threading
from pg_training import train
from play import run_simulation
from environment.custom_env import WasteCollectionEnv
from environment.rendering import render_environment

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='train', 
                        help="Choose 'train', 'simulate', or 'render'")
    args = parser.parse_args()
    
    if args.mode == 'train':
        train()
    elif args.mode == 'simulate':
        run_simulation()
    elif args.mode == 'render':
        env = WasteCollectionEnv()
        # Run the graphical rendering in a separate thread.
        threading.Thread(target=render_environment, args=(env,)).start()
    else:
        print("Invalid mode selected. Choose 'train', 'simulate', or 'render'.")

if __name__ == '__main__':
    main()
