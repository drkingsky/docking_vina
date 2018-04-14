import sys, re

exp = sys.argv[1]
score_dict = {}
with open('score.sc', 'rb') as f:
    for num,line in enumerate(f):
        if num > 1:
            line = line.strip().split()
            id = line[-1]
            rosetta_score = line[1]
            if not score_dict.has_key(id):
                score_dict[id] = []
            score_dict[id].append(rosetta_score)
            
for i in range(1,101):
    score_file = 'cnb2_rem_input_0%03d_dock_log'%i
    id = 'cnb2_rem_input_0%03d'%i
    with open(score_file, 'rb') as f:
        content = f.read()
        p = re.compile(r'----------\n(.+?)\nWriting')
        dock_socre = re.findall(p, content)[0].split()[1]
        print dock_socre
        score_dict[id].append(dock_socre)
        
with open('vina_rosetta_exp%s.sc'%exp, 'wb') as f:
    #f.write('\t'.join(['Protein_ID', 'rosetta_score', 'vina_score']) + '\n')
    for key, value in score_dict.iteritems():
        f.write('exp%s_'%exp + key + '\t' + '\t'.join(value) + '\n')
        