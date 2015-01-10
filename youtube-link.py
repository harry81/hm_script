# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, sys, getopt
import re
import subprocess
import urllib2

class GetLink():
    def __init__(self, link):
        self.root_link = link
        self.tmp_file = '/tmp/youtube.html'

    def create_html(self):
        cmd = "curl http://www.youtube.com/watch?v={} > /tmp/youtube.html".format(self.root_link)
        url = "http://www.youtube.com/watch?v={}".format(self.root_link)
        content = urllib2.urlopen(url).read()
        fp = open(self.tmp_file,'wt').write(content)

    def get_youtube_id(self):
        self.create_html()
        fp = open('/tmp/youtube.html')
        content = fp.read()
        pat = re.compile(ur'/watch\?v=([a-zA-Z0-9]+)\"')
        m = pat.findall(content)
        self.links = list(set(m))
        
    def download_mp3(self, test=False):
        self.get_youtube_id()
        for link in self.links[:10]:
            cmd = "/usr/bin/youtube-dl --extract-audio --audio-format mp3 -o /home/harry/Music/%(title)s.%(ext)s {}".format(link)
            if test==False:
                popen = subprocess.Popen(cmd.split(),
                                        shell=False,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            self.remove_html()
        
    def remove_html(self):
        try:
            os.remove(self.tmp_file)
        except OSError:
            pass
    

def main(argv):
    gl = GetLink(argv[0])    
    gl.download_mp3()

if __name__ == '__main__':
    main(sys.argv[1:])
