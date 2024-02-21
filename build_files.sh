echo "BUILD START"
python3.12.0 -m pip install -r requirement.txt
python3.12.0 manage.py collectstatic --noinput --clear
echo "BIULD END"