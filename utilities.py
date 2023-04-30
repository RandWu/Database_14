import re
import hashlib
from datetime import datetime

sex_constraints = ["F", "M", "O"]
role_constraints = ["admin", "student"]

def check_input(string: str) -> bool:
    pattern = re.compile(r"^[a-zA-Z0-9_]+$")
    if not pattern.match(string):
        return False
    else:
        return True
    
def check_number(value: int, ranges: range = None) -> bool:
    boolz = isinstance(value, (int, float))
    if ranges is not None and boolz:
        return value in ranges
    return boolz
    
def sha1_hash(string: str) -> str:
    return hashlib.sha1(string.encode()).hexdigest()

def datetime_format(input_date: datetime) -> str:
    return input_date.strftime(r'%Y-%m-%d %H:%M:%S')

def str_to_datetime(string: str) -> datetime:
    return datetime.fromisoformat(string)

def get_current_time() -> datetime:
    return datetime.now()

def constraint(category: str, value) -> bool:
    if category == "sex":
        return str(value) in sex_constraints
    if category == "role":
        return str(value) in role_constraints
