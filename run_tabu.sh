#!/bin/bash
python main.py datasets/scp42.txt 4_2-1-tabu 0.003 3600 TabuSearch


python main.py datasets/scp41.txt 4_1-2-tabu 0.005 3600 TabuSearch
python main.py datasets/scp41.txt 4_1-3-tabu 0.008 3600 TabuSearch
python main.py datasets/scp41.txt 4_1-4-tabu 0.010 3600 TabuSearch

python main.py datasets/scp41.txt 4_2-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp42.txt 4_2-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp43.txt 4_3-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp44.txt 4_4-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp45.txt 4_5-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp46.txt 4_6-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp47.txt 4_7-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp48.txt 4_8-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp49.txt 4_9-4-tabu 0.010 3600 TabuSearch
python main.py datasets/scp410.txt 4_10-4-tabu 0.010 3600 TabuSearch