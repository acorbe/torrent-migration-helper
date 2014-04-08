#!/usr/bin/env python  
"""torrent_migration_helper

given a folder containing a set A of .torrent files,
      a folder containing a set B of downloaded files,
      [a string STR which is expected to be in the final torrent tracker name]

a subset of .torrent in A such that
      the torrent has been downloaded in B
      [the tracker of the torrent contains STR]
is copied in a target folder.

This answers to a common need. Whenever a folder containing a downloaded torrents to be seeded needs to be migrated in another seeding server, specific .torrent files need to be selected and added to destination torrent client. This package helps to make such process automatic.

"""

import os
import pandas as pd
import torrentparse as tp
import shutil


__author__ = "Alessandro Corbetta"
__copyright__ = "Copyright 2014, Alessandro Corbetta"

__license__ = "GPL"
__version__ = ".1"
__maintainer__ = "Alessandro Corbetta"
__email__ = "corbisoft dot codes at gmail dot com"




DEFAULT_PATH = './torrentfile_source/'
DEFAULT_F_EXT = '.torrent'


def list_dir(path = DEFAULT_PATH 
                  , print_list = False
                  , fending = '.torrent'
             , just_files = True ):
"""lists the content of a given dir (path).

   One can specify the ending (fending = '.torrent') of the considered files/dirs (defaulted to .torrent).
   One can specify whether to include just files and skip directories (just_files = True). """
    
    print "acquiring file list..."
    
    if just_files:
        flist = [ (f,os.path.join(path,f)) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and f.endswith(fending) ]
    else:
        flist = [ (f,os.path.join(path,f)) for f in os.listdir(path) if f.endswith(fending) ]
    if print_list:
        for f,fp in flist:
            print fp

    print "done!"    
    return flist

def build_df_from_flist(path
                        , flist = None                        
                        , default_ext = DEFAULT_F_EXT ):
    
"""Builds a pandas DataFrame whose records are .torrent information. 
In particular:

       fname (full name of the file)
       fpath (full path of the file) 
       TorrentParser (TorrentParser object)
       TrackerUrl
"""
    if flist is None:
        flist = list_dir(path)

    flist_df = pd.DataFrame(flist, columns = ['fname','fpath'])
    flist_df['fname_plain'] = flist_df.fname.apply( lambda f : f[:-len(default_ext)])

    def parseTorrent(r):
        """calls TorrentParser constructor on each torrent file"""
        try:
            ret = tp.TorrentParser(r['fpath'])
        except:
            ret = None
        return ret

    print "parsing torrents..."

    flist_df['TorrentParser'] = flist_df.apply( parseTorrent, axis = 1 )    
    print "extracting trackers..."
    def get_tracker(r):
        if r is not None:
            try:
                return r['TorrentParser'].get_tracker_url()
            except:
                return ''
        else:
            return ''

    flist_df['TrackerUrl'] = flist_df.apply( get_tracker , axis = 1 )

    print "done!"
    
    return flist_df

def parse_tracker_list(flist_df
                       , substr
                       , output_filtered_torrent_list = False ):
    """filters the pd.DataFrame containing the .torrent files information and retains
    the ones whose tracker address contains substr.
    returns the filtered pd.DataFrame.    
    """

    flist_flt = flist_df[flist_df.TrackerUrl.apply(lambda st : substr in st)]

    if output_filtered_torrent_list:
        sorted_flist = flist_flt.fname    
        sorted_flist.order().to_csv('output.csv')
        
    return flist_flt

def gather_downloaded_files(path):
    """retrieves the full list of files and dirs in path"""

    flist = list_dir(path = path
                     , fending = ''
                     , just_files = False)

    flist_names_set = set([f for f,fp in flist])
    return {'fnames' : flist , 'fnames_set' : flist_names_set}
    
def filter_torrent_in_given_dl_site(flist_df,dl_site_content):
    """determines which .torrents (rows in flist_df np.DataFrame) are actually in the
    download site (df_site_content)"""
    
    print "filtering for dl site..."
    matching = flist_df.fname_plain.apply(lambda fn : fn in dl_site_content['fnames_set'])
    print "done"
    return matching


def main(tor_fl_source
         , tor_fl_dest
         , tor_dl_source
         , tracker_address_content = None ):
    """core function. The following steps are performed
         1. a database DB out of .torrent files in tor_fl_source is built
         2. the database DB is filtered based on which trackers contain in their
            address the string tracker_address_content
         3. the download site (tor_dl_source) is scanned and a set with the file names is built
         4. the elements of DB which have a correspondence in the download site are identified
         5. Indentified .torrents are copied in folder tor_fl_dest
    """
    
    #builds database of torrent files
    df = build_df_from_flist(tor_fl_source)
    
    #possibly restricts torrent database considering just trackers having a particular string in their address
    if tracker_address_content is not None:    
        df_fl = parse_tracker_list(df,tracker_address_content)
    else:
        df_fl = df

    #builds the database of the download target directory
    df_dl = gather_downloaded_files(tor_dl_source)

    #extracts the intersection between the torrent files list and the files actually downloaded (based on the file name)
    matching1 = filter_torrent_in_given_dl_site(df_fl,df_dl)

    #obtains the list of .torrent files from matching1 
    df_fl1 = df_fl[matching1]

    #copies selected .torrent files in destination path
    df_fl1.fpath.apply(lambda pt : shutil.copy(pt,tor_fl_dest))

if __name__ == '__main__':

    tor_dl_source = '/downloaded/torrent/location/'
    
    tor_fl_source = '/torrent/file/source/'
    tor_fl_dest = '/torrent/file/destination/'

    tracker_address_content = 'tracker_address_content'

    main(tor_fl_source, tor_fl_dest, tor_dl_source , tracker_address_content)
