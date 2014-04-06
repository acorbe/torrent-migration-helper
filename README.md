torrent-migration-helper
========================

Given a folder containing `.torrent` files `S`, and a second folder where `.torrent`s (possibly different) have been downloaded `D`, it identifies which files in `S` have been downloaded in `D`.

Further restricyions on the tracker of desired files in `S` can be imposed.

This is primarily aimed at facilitating torrent seeding migration from a given folder/hard drive/machine to a second folder/hard drive/machine.

Dependencies:

  + [torrentparse](https://github.com/mohanraj-r/torrentparse) by [mohanraj-r](https://github.com/mohanraj-r) which is supposed to be installed. Please check upon [my fork](https://github.com/acorbe/torrentparse).
  + pandas, as the set of torrent files is memorized in a python dataframe and thereby queried.

Tipical use:
  + TBC    
