import re
import hashlib
from datetime import datetime

sex_constraints = ["F", "M", "O"]
role_constraints = ["admin", "student"]

def check_input(string: str) -> bool:
    pattern = re.compile(r"^[a-zA-Z0-9\s_.,'-]+$")
    if not pattern.match(string):
        return False
    else:
        return True
    
def is_pattern_valid(pattern: str) -> bool:
    try:
        # Try to compile the pattern using Python's regex engine
        re.compile(pattern)
        # Escape backslashes
        pattern = pattern.replace('\\', '\\\\')
        return True if re.search(r'^\w+$', pattern) else False
    except re.error:
        return False

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

def scholarship_to_display(all: list, applied: list) -> list:
    applied_ids = {x[0] for x in applied} 
    filtered_all = [y for y in all if y[0] not in applied_ids]
    lod1 = [dict(zip(['id', 'name', 'rank', 'year', 'issuer', 'status'], t)) for t in applied]
    lod2 = [dict(zip(['id', 'name', 'rank', 'year', 'issuer', 'status'], u + ('TODO',))) for u in filtered_all]
    return lod1 + lod2

def constraint(category: str, value) -> bool:
    if category == "sex":
        return str(value) in sex_constraints
    if category == "role":
        return str(value) in role_constraints
