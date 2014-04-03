import os
import pandas as pd
import torrentparse as tp
import shutil

DEFAULT_PATH = './torrentfile_source/'
DEFAULT_F_EXT = '.torrent'


def list_dir(path = DEFAULT_PATH 
                  , print_list = False
                  , fending = DEFAULT_F_EXT
            , just_files = True ):
    
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
    
    if flist is None:
        flist = list_dir(path)

    flist_df = pd.DataFrame(flist, columns = ['fname','fpath'])
    flist_df['fname_plain'] = flist_df.fname.apply( lambda f : f[:-len(default_ext)])

    def parseTorrent(r):
        try:
            ret = tp.TorrentParser(r['fpath'])
        except:
            ret = None
        return ret

    print "parsing torrents..."
    flist_df['TorrentParser'] = flist_df.apply( parseTorrent , axis = 1)
    
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

def parse_tracker_list(flist_df,substr):

    flist_flt = flist_df[flist_df.TrackerUrl.apply(lambda st : substr in st)]
    sorted_flist = flist_flt.fname
    sorted_flist.order().to_csv('output.csv')
    return flist_flt

def gather_downloaded_files(path):
    flist = list_dir(path = path
                     , fending = ''
                     , just_files = False)

    flist_names_set = set([f for f,fp in flist])
    return {'fnames' : flist , 'fnames_set' : flist_names_set}
    
def filter_torrent_in_given_dl_site(flist_df,dl_site_content):

    print "filtering for dl site..."
    matching = flist_df.fname_plain.apply(lambda fn : fn in dl_site_content['fnames_set'])
    print "done"
    return matching


def main(tor_fl_source
         , tor_fl_dest
         , tor_dl_source
         , tracker_address_content = None ):

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
