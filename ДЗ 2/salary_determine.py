import re

def salary_determine(str):
    work_salary_dict = {'salary_start': None, 'salary_end': None, 'valute': None}
    if str:
        str = str.replace(u'\u202f', u'')
        pattern = re.compile(r'^от (?P<salary_start1>[0-9]+) (?P<valute1>([\w]+))|^до (?P<salary_end1>[0-9]+) (?P<valute2>([\w]+))|(?P<salary_start2>[0-9]+) – (?P<salary_end2>[0-9]+) (?P<valute3>([\w]+))', re.IGNORECASE)
        m = pattern.match(str)
        if m:
            if m.group('salary_start1') or m.group('salary_start2'):
                work_salary_dict['salary_start'] = int(m.group('salary_start1') or m.group('salary_start2'))
            if m.group('salary_end1') or m.group('salary_end2'):
                work_salary_dict['salary_end'] = int(m.group('salary_end1') or m.group('salary_end2'))
            work_salary_dict['valute'] = m.group('valute1') or m.group('valute2') or m.group('valute3')
    
    return work_salary_dict

def salary_determine_2(str):
    work_salary_dict = {'salary_start': None, 'salary_end': None, 'valute': None}
    if str:
        str = str.replace(u'\u202f', u'')
        pattern = re.compile(r'от (?P<salary_start2>[0-9]+) до (?P<salary_end2>[0-9]+) (?P<valute3>([\w]+))|^от (?P<salary_start1>[0-9]+) (?P<valute1>([\w]+))|^до (?P<salary_end1>[0-9]+) (?P<valute2>([\w]+))', re.IGNORECASE)
        m = pattern.match(str)
        if m:
            if m.group('salary_start1') or m.group('salary_start2'):
                work_salary_dict['salary_start'] = int(m.group('salary_start1') or m.group('salary_start2'))
            if m.group('salary_end1') or m.group('salary_end2'):
                work_salary_dict['salary_end'] = int(m.group('salary_end1') or m.group('salary_end2'))
            work_salary_dict['valute'] = m.group('valute1') or m.group('valute2') or m.group('valute3')
    
    return work_salary_dict

# print(salary_determine('от 250\u202f000 руб.'))
# print(salary_determine('до 220\u202f000 руб.'))
# print(salary_determine('170\u202f000 – 220\u202f000 руб.'))
# print(salary_determine('170\u202f000 – 220\u202f000 USD'))
# print(salary_determine(None))

print(salary_determine_2('от 250\u202f000 руб.'))
print(salary_determine_2('до 220\u202f000 руб.'))
print(salary_determine_2('от 170\u202f000 до 220\u202f000 руб.'))