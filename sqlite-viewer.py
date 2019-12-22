#!/usr/bin/env python3
import sqlite3
import sys
import shutil
import textwrap

if len(sys.argv) < 2:
    print('not enough args')
    sys.exit(1)

conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()

sql = ''
if len(sys.argv) == 4 and sys.argv[2] == '-count':
    expr = sys.argv[3]
    table, columns = expr.split(':')
    sql = 'select {columns}, count(1) as count from {table} group by {columns} order by count(1) desc'.format(table=table, columns=columns)
else:
    sql = sys.argv[2] if len(sys.argv) == 3 else sys.stdin.read().strip()

# make the first row the columns headings
try:
    c.execute(sql)
except sqlite3.Error as e:
    print('sqlite error: ' + str(e))
    conn.close()
    sys.exit(1)
rows = [tuple(x[0] for x in c.description)]

c.arraysize = 25
results = c.fetchmany()
results = list(map(lambda r: tuple('null' if x is None else str(x) for x in r), results))
rows.extend(results)
conn.close()

lengths = [0] * len(rows[0])
term_width = shutil.get_terminal_size().columns
delimiter = '  '

# figure out the max lengths per column
for row in rows:
    for idx, col in enumerate(row):
        if len(col) > lengths[idx]:
            lengths[idx] = len(col)

width_needed = sum(lengths) + (len(lengths) * len(delimiter))
if width_needed >= term_width:
    # we don't have enough space, evenly distribute the column widths
    # lengths = [int(width_needed / len(lengths))] * len(lengths)
    extra_width = width_needed - term_width
    max_idx = 0
    for idx, length in enumerate(lengths):
        if length > lengths[max_idx]:
            max_idx = idx
    lengths[max_idx] -= extra_width

for row_idx, row in enumerate(rows):
    if row_idx == 0:
        sys.stdout.write('\x1b[96m')

    next_lines = []
    for idx, col in enumerate(row):
        wrapped = textwrap.wrap(col, width=lengths[idx])
        sys.stdout.write(wrapped[0].ljust(lengths[idx]))
        if len(wrapped) > 1:
            # push the new lines to next_lines so they can be rendered after the current one
            for line_idx, line in enumerate(wrapped[1:]):
                l = (' ' * sum(lengths[:idx])) + ('  ' * idx) + line.ljust(lengths[idx])
                next_lines.append(l)
        sys.stdout.write('  ')

    for line in next_lines:
        sys.stdout.write('\n')
        sys.stdout.write(line);

    if row_idx == 0:
        sys.stdout.write('\x1b[0m')
    sys.stdout.write('\n')
