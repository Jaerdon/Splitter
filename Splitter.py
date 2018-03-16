import sys

file = None

if (len(sys.argv) > 1):
    file = sys.argv[1]
else:
    file = input("Enter file path:")

with open(file, 'r', encoding='utf8') as f:
    lines = f.read().splitlines()

t0 = open(file[:5] + '_T0.gcode', 'w')
t1 = open(file[:5] + '_T1.gcode5', 'w')

tool = 0
offset = 20.0

def find(val, args):
    i = 0
    while (i < len(args)):
        if (args[i].startswith(val)):
            return i
        else:
            i += 1
    return len(args)
            

for line in lines:
    #print(line)
    if (line.startswith('T')):
        tool = int(line[-1])
    elif (line.startswith('G1') or line.startswith('G0')):
        args = line.split(';')[0].strip().split(' ')
        f = find('F', args)
        x = find('X', args)
        y = find('Y', args)
        z = find('Z', args)
        e = find('E', args)
        
        args.append('')

        #print(args)

        if (tool == 0):
            t0.write((args[0] + ' ' + args[f] + ' ' + args[x] + ' ' + args[y] + ' ' + args[z] + ' ' + args[e] + '\n').replace('  ', ' '))
            argsx = args[x].replace('X', 'X-').replace('--', '')
            if y is not len(args) - 1:
                argsy = 'Y' + str(float(args[y].replace('Y', 'Y-').replace('--', '')[1:]) - offset)
            else:
                argsy = ''
            t1.write((args[0] + ' ' + args[f] + ' ' + argsx + ' ' + argsy + ' ' + args[z] + ' E0' + '\n').replace('  ', ' '))
        else:
            if y is not len(args) - 1:
                argsy = 'Y' + str(float(args[y][1:]) - offset)
            else:
                argsy = ''
            t0.write((args[0] + ' ' + args[f] + ' ' + args[x] + ' ' + argsy + ' ' + args[z] + ' E0' + '\n').replace('  ', ' '))
            argsx = args[x].replace('X', 'X-').replace('--', '')
            argy = args[y].replace('Y', 'Y-').replace('--', '')
            t1.write((args[0] + ' ' + args[f] + ' ' + argsx + ' ' + argy + ' ' + args[z] + ' ' + args[e] + '\n').replace('  ', ' '))
    else:
        t0.write(line + '\n')
        t1.write(line + '\n')

t0.close()
t1.close()
