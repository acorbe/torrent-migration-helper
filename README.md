torrent-migration-helper
========================

Given a folder containing `.torrent` files `S`, and a second folder where `.torrent`s (possibly different) have been downloaded `D`, it identifies which files in `S` have been downloaded in `D`.

Further restricyions on the tracker of desired files in `S` can be imposed.

This is primarily aimed at facilitating torrent seeding migration from a given folder/hard drive/machine to a second folder/hard drive/machine.

Dependencies:

  + [torrentparse](https://github.com/mohanraj-r/torrentparse) by [mohanraj-r](https://github.com/mohanraj-r) which is supposed to be installed. ([my fork](https://github.com/acorbe/torrentparse) in case of unevenness).
  + [pandas](http://pandas.pydata.org/), as the set of torrent files is memorized in a python dataframe and thereby queried.

------------------

**Tipical use:**

You have an hard drive where a number of torrents have been downloaded and are currently seeded. 

One day, you need to migrate this hard drive to a second machine which will handle the seeding from now on.

In order to get on with the seeding, you need to add to the torrent client the `.torrent` files referring to the downloaded files in the disk.

In the original machine you certainly have a folder where all the `.torrent` have been cached, hence you need to select all the `.torrent` files you actually need.

Moreover, you might need to consider just the `.torrent` referring to given trackers or so.


This small application allows you to do so easily.

-----------------

TODO:

   + UI is at the moment done via modification of three strings in the main part of the script. This has to be changed with a standard command line interaction.

