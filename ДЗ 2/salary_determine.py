import re

def salary_determine(str):
    work_salary_dict = {}
    pattern = re.compile(r'^от (?P<salary_start>([\w\.-]+))\u202f([\w\.-]+) (?P<valute>([\w\.-]+))', re.IGNORECASE)
    if not pattern.match(str):
        pattern = re.compile(r'^до (?P<salary_end>([\w\.-]+))\u202f([\w\.-]+) (?P<valute>([\w\.-]+))', re.IGNORECASE)
        if not pattern.match(str):
            pattern = re.compile(r'(?P<salary_start>([\w\.-]+))\u202f([\w\.-]+) – (?P<salary_end>([\w\.-]+))\u202f([\w\.-]+) (?P<valute>([\w\.-]+))', re.IGNORECASE)
            if not pattern.match(str):
                return 'error'
    # ([\w\.-]+)@([\w\.-]+)
    return pattern.match(str).groupdict()

print(salary_determine('от 250\u202f000 руб.'))
print(salary_determine('до 220\u202f000 руб.'))
print(salary_determine('170\u202f000 – 220\u202f000 руб.'))