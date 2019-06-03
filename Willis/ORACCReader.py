import json, pprint
from oracc_reader import ORACC_text_reader

with open('Q003475.json', encoding="utf8") as f:
    json_text = f.read()
tr = ORACC_text_reader(json_text)
for c, t, n in zip(tr.output_cuneiform(),
                   tr.output_translit(with_line_headers=False),
                   tr.output_norm(with_line_headers=False)):
    line_header = ' '.join(c.split()[:2])
    spacing = ' ' * len(line_header)
    print(line_header + ' ' + ' '.join(c.split()[2:]))
    if t != '': print(spacing + t)
    if n != '': print(spacing + n)