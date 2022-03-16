pushd .
cd ..
call venv\Scripts\activate.bat
python -m black -l 192 multiprocessing_talk workers
call deactivate
popd
