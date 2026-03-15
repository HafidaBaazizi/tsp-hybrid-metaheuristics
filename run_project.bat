@echo off
python scriptsun_experiments.py --data-dir data	splib --output resultsaw_results.csv --runs 2 --seed 42 --solutions data	splib\solutions.txt
python scripts\summarize_results.py --input resultsaw_results.csv --summary results\summary_results.csv --latex report	ables_generated_results.tex --figure-dir resultsigures
pause
