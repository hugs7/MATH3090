@echo off

jupyter nbconvert --to latex "Assignment 2\MATH3090 Assignment 2.ipynb" --output-dir "Assignment 2\tex-aux"

pause
xelatex "Assignment 2\tex-aux\MATH3090 Assignment 2.tex" -output-directory="Assignment 2" -aux-directory="Assignment 2\tex-aux"

pause
