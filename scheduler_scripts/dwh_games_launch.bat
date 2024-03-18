set CONDAPATH=C:\Users\Admin\anaconda3
rem https://gist.github.com/maximlt/531419545b039fa33f8845e5bc92edd6
rem Define here the name of the environment
set ENVNAME=Chess

rem The following command activates the base environment.
rem call C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate the conda environment
rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

rem Run a python script in that environment
python dwh_games.py

rem Deactivate the environment
call conda deactivate
pause