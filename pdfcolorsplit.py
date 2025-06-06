#!/usr/bin/env python
# Python 2 and 3 compatible.

# Python program to take a pdf file, and split it into color and black
# and white part(s). Requires pdftk and one of gs and pdftoppm.
#
# Iain Murray, February 2010.
#
# Inspired by dvicoloursplit.py, Jeremy Sanders 2001, although written
# from scratch.
#
# 2011-09-19 fixed bug with odd numbers of pages reported by Richard Shaw
# 2012-06-11 tweaked to run in Python 3 as well as 2.

##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.

import os, os.path, sys, string, re, tempfile, shutil, getopt
import heapq

def a2b(x):
    """Turn ascii into bytes for Python 3, in way that works with Python 2"""
    try:
        return bytes(x)
    except:
        return bytes(x, 'ascii')

def iscolorppm(filename):
    """Does the PPM file contain any non-grayscale colors?"""
    file = open(filename, 'rb')
    # Ugly: I read the whole file into RAM, and copy it needlessly a lot
    data = file.read()
    file.close()

    # PPM is a *very* liberal file format. It allows comments anywhere in the
    # header, even in the middle of tokens.
    comments_re = re.compile(a2b('^([^ \t\n]*)#[^\n]*\n'))
    split_re = re.compile(a2b('^([ \t\n]|#[^\n]*\n)+([^ \t\n#])'))
    tok_re = re.compile(a2b('^([^ \t\n]*)([ \t\n].*)'), re.DOTALL)
    toks = []
    while len(toks) < 4:
        while split_re.match(data):
            data = split_re.sub(r'\2', data)
        while comments_re.match(data):
            data = comments_re.sub(r'\1', data)
        (tok, data) = tok_re.match(data).groups()
        toks.append(tok)
    magic = toks[0]
    (width, height, max_color) = map(int, toks[1:])
    data = data[1:]

    if magic == b'P3':
        binary = False
    elif magic == b'P6':
        binary = True
    else:
        print("%s is not a valid PPM file" % filename)
        sys.exit(1)

    # Massage data so adjacent triples should have the same value in b/w images
    data_len = width*height*3
    if binary:
        if int(max_color) > 255:
            # Untested. Each intensity is in two bytes.
            data_len *= 2
            data = data[1:data_len:2] + data[:data_len:2]
    else:
        data = [int(x) for x in data.split()]

    if len(data) < data_len:
        print('PPM file is truncated?')
        sys.exit(1)

    triples = zip(data[0:data_len:3], data[1:data_len:3], data[2:data_len:3])
    black_and_white = all((a==b and a==c for (a,b,c) in triples))
    return not black_and_white


def pdfcolorsplit(file, doublesided, merge, use_pdftoppm, reassemble, verbose):
    # Work out which pages are color
    if verbose:
        print('Analyzing %s...' % file)
    tmpdir = tempfile.mkdtemp(prefix = 'pdfcs_')
    if use_pdftoppm:
        root = os.path.join(tmpdir, 'page')
        os.system('pdftoppm -r 20 "%s" "%s"' % (file, root))
    else:
        gs_opts = '-sDEVICE=ppmraw -dBATCH -dNOPAUSE -dSAFE -r20'
        if not verbose:
            gs_opts += ' -q'
        os.system('gs ' + gs_opts + ' -sOutputFile="%s" "%s"' \
                % (os.path.join(tmpdir, 'tmp%06d.ppm'), file))
    PPMs = os.listdir(tmpdir)
    PPMs.sort()
    iscolor = [iscolorppm(os.path.join(tmpdir, x)) for x in PPMs]
    num_pages = len(iscolor)
    shutil.rmtree(tmpdir)
    if doublesided:
        # Treat as color those b/w pages that share a sheet with a color page
        iscolorpair = [x or y for (x,y) in zip(iscolor[::2], iscolor[1::2])]
        iscolor[:2*len(iscolorpair):2] = iscolorpair
        iscolor[1::2] = iscolorpair

    # Construct page range strings
    flips = [x for x in range(2,num_pages+1) if iscolor[x-1] != iscolor[x-2]]
    if not flips:
        if verbose:
            print('No splitting needs to be done, skipping %s' % file)
        return
    edges = [1] + flips + [num_pages+1]
    ranges = ['%d-%d' % (x,y-1) for (x,y) in zip(edges[:-1], edges[1:])]

    print(iscolor, ranges)
    currentcolor = iscolor[0]
    print('Color pages:')
    for i in range(len(ranges)):
        if currentcolor:
            print(ranges[i])
        currentcolor = not currentcolor

    # Finally output split files
    if verbose:
        print('Outputing splits as new pdf files...')
    base_name = file
    if base_name.lower().endswith('.pdf'):
        base_name = base_name[:-4]
    suffixes = ['_bwsplit', '_colorsplit']
    # jobs is a seq of (range, filename) pairs, e.g. ('1-3', 'colorbits.pdf')
    # convert jobs
    if merge:
        jobs = ((' '.join(ranges[0::2]), base_name + suffixes[iscolor[0]]),\
                (' '.join(ranges[1::2]), base_name + suffixes[not iscolor[0]]))
    else:
        jobs = [(r, '%s_%03d%s' % (base_name,n+1,suffixes[(n+iscolor[0])%2])) \
                for (n,r) in enumerate(ranges)]



    for (pages, name) in jobs:
        if verbose:
            print('pdftk "%s" cat %s output "%s.pdf"' % (file, pages, name))
        os.system('pdftk "%s" cat %s output "%s.pdf"' % (file, pages, name))

    # reassemble all continuous files into final output by converting b/w parts to grayscale
    if reassemble:
      graySuffix = "_gray"
      jobsconvert = [ j for j in jobs[ int(iscolor[0])::2] ]
      #print(jobsconvert)
      # convert all b/w to gray
      for (pages,name) in jobsconvert:
        cmd="gs  -sOutputFile=%s%s.pdf  -sDEVICE=pdfwrite  -dAutoRotatePages=/None -sColorConversionStrategy=Gray  -dProcessColorModel=/DeviceGray  -dCompatibilityLevel=1.4  -dNOPAUSE  -dBATCH %s.pdf" % (name,graySuffix,name)
        if verbose:
           print(cmd) 
        os.system(cmd)

      ## interleave converted b/w and colors and make pdftk cat command
      cJobs = jobs[0::2] if iscolor[0] else jobs[1::2]
      #print(cJobs)
      bwJobs = [ (pages,name+graySuffix) for pages,name in jobsconvert]

      def interleave(l1, l2):
        iter1 = iter(l1)
        iter2 = iter(l2)
        while True:
            try:
                if iter1 != None:
                    yield next(iter1)
            except StopIteration:
                iter1 = None
            try:
                if iter2 != None:
                    yield next(iter2)
            except StopIteration:
                iter2 = None
            if iter1 == None and iter2 == None:
                raise StopIteration()


      jobsCatAll = interleave(cJobs,bwJobs) if iscolor[0] else interleave(bwJobs,cJobs)
      #print(list(jobsCatAll))

      cmd = "pdftk " + " ".join([j[1]+".pdf" for j in jobsCatAll]) + " cat output %s%s.pdf " % (base_name,"_all")
      if verbose:
        print(cmd)  
      os.system(cmd)

def usage():
    progname = os.path.basename(sys.argv[0])
    print('Usage: %s [OPTIONS] <PDF-file(s)>' % progname)
    print('')
    print('Splits PDF files into color and black and white sections.')
    print('')
    print('Options:')
    print('   -m option merges color and b/w parts to give two files.')
    print('      The default is to output numbered contiguous pieces')
    print('      that could easily be reassembled.')
    print('   -s option chooses simplex rather than duplex output')
    print('   -v verbose.')
    print('   -p Use pdftoppm rather than gs to detect color. Faster,')
    print('      but can get confused by hyperlinks that do not print.')
    print('   -r Reassemble all continuous files by converting all b/w ')
    print('      parts to grayscale (requires gs).')

def main():
    try:
        opt_pairs, filenames = getopt.gnu_getopt(sys.argv[1:], "hvpmsr", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(1)
    if opt_pairs:
        opts = list(zip(*opt_pairs))[0]
    else:
        opts = []
    if ('-h' in opts) or ('--help' in opts) or (not filenames):
        usage()
        sys.exit()
    verbose = '-v' in opts
    use_pdftoppm = '-p' in opts
    merge = '-m' in opts
    doublesided = not ('-s' in opts)

    reassemble = '-r' in opts

    if merge and reassemble:
      raise ValueError("Merge and reassemble options not compatible!")

    for file in filenames:
        pdfcolorsplit(file, doublesided, merge, use_pdftoppm, reassemble, verbose)

if __name__ == "__main__":
    main()
