#! /usr/bin/env python
#
#   script generator for project="2021-S1-MX-26"
#

import os
import sys

project="2021-S1-MX-26"

#        obsnums per source (make it negative if not added to the final combination)
#  initial test cases are J113833 and J132227 (where the J was accidentally dropped from the name)
on = {}
on['IRAS13349+2438']  = [100398, 100399, 100400, 100402, 100403, 100404, 100406, 100407, 100408]


on['PG_1448+273'] = [100431, 100432, 100433, 100435, 100436, 100437, 100439, 100440, 100441]


#        common parameters per source on the first dryrun (run1, run2)
#        1/1,3,3 are bad for all the series
#        3/5 was bad until Gopal reseated : on 5-may-2022 ?
pars1 = {}
common1="admit=0 restart=1 badcb=1/1,3/3"
pars1['IRAS13349+2438']  = ""
pars1['PG_1448+273'] = ""

#        common parameters per source on subsequent runs (run1a, run2a)
pars2 = {}
common2="admit=0 restart=1 srdp=1"
pars2['IRAS13349+2438']  = ""
pars2['PG_1448+273'] = ""



# below here no need to change code
# ========================================================================

#        helper function for populating obsnum dependant argument -- deprecated
def getargs3(obsnum):
    """ search for <obsnum>.args
    """
    f = "%d.args" % obsnum
    if os.path.exists(f):
        lines = open(f).readlines()
        args = ""
        for line in lines:
            if line[0] == '#': continue
            args = args + line.strip() + " "
        return args
    else:
        return ""

#        specific parameters per obsnum will be in files <obsnum>.args -- deprecated
pars3 = {}
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        pars3[o] = getargs3(o)

#        obsnum.args is alternative single file pars file to set individual parameters
pars4 = {}
if os.path.exists("obsnum.args"):
    lines = open("obsnum.args").readlines()
    for line in lines:
        if line[0] == '#': continue
        w = line.split()
        pars4[int(w[0])] = w[1:]
        print('PJT',w[0],w[1:])

def getargs(obsnum):
    """ search for <obsnum> in obsnum.args
    """
    args = ""
    if obsnum in pars4.keys():
        print("PJT2:",obsnum,pars4[obsnum])
        for a in pars4[obsnum]:
            args = args + " " + a
    return args

run1  = '%s.run1'  % project
run1a = '%s.run1a' % project
run1b = '%s.run1b' % project
run2  = '%s.run2' % project
run2a = '%s.run2a' % project

fp1 = open(run1,  "w")
fp2 = open(run1a, "w")
fp3 = open(run1b, "w")

fp4 = open(run2,  "w")
fp5 = open(run2a, "w")

#                           single obsnum
n1 = 0
for s in on.keys():
    for o1 in on[s]:
        o = abs(o1)
        cmd1 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 restart=1 %s %s" % (o,s,pars1[s], pars2[s], getargs(o))
        cmd2 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 restart=1" % (o,s,pars1[s])
        cmd3 = "SLpipeline.sh obsnum=%d _s=%s %s admit=0 %s" % (o,s,pars2[s], getargs(o))
        fp1.write("%s\n" % cmd1)
        fp2.write("%s\n" % cmd2)
        fp3.write("%s\n" % cmd3)
        n1 = n1 + 1

#                           combination obsnums
n2 = 0        
for s in on.keys():
    obsnums = ""
    n3 = 0
    for o1 in on[s]:
        o = abs(o1)
        if o1 < 0: continue
        n3 = n3 + 1
        if obsnums == "":
            obsnums = "%d" % o
        else:
            obsnums = obsnums + ",%d" % o
    print('%s[%d/%d] :' % (s,n3,len(on[s])), obsnums)
    cmd4 = "SLpipeline.sh _s=%s admit=0 restart=1 obsnums=%s" % (s, obsnums)
    cmd5 = "SLpipeline.sh _s=%s admit=1 srdp=1  obsnums=%s" % (s, obsnums)
    fp4.write("%s\n" % cmd4)
    fp5.write("%s\n" % cmd5)
    n2 = n2 + 1

print("A proper re-run of %s should be in the following order:" % project)
print(run1a)
print(run2)
print(run1b)
print(run2a)
print("Where there are %d single obsnum runs, and %d combination obsnums" % (n1,n2))

