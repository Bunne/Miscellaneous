Killing Floor Whitelist Map Installer
=======================================
A rewrite of my original KF command-line tool.

Requires Python 3.

Configuration
-------------
Little additional configuration should be necessary to run the script. However, you may need to adjust the path in the config file to point to your own Killing Floor installation. Just make sure that it points to the root Killing Floor directory containing all the Map, Texture (etc.) folders. OS X users may use '%s' in place of their username, the installer will fill it in.

Use
---
#### Listing Maps
View what maps you have installed (mine), maps not installed (diff), and maps available for download (online).
    
    KF.py view <mine | online | diff>
    
#### Viewing Map Info
Get info on maps and view them online. The given name does not need to be a complete match.
    
    KF.py info <name>

**Example:**

    $ KF.py info Containment
    Name: KF-ContainmentStation
    Author: Fel
    Link: http://sykosis.co.uk/kfmwhitelist/1433/kf-containmentstation
    Info: KF-ContainmentStation - 4195 downloads - 15.58 MB zip
    
#### Installing Maps
Install maps quickly for immediate use in-game. The name must be a complete match, with or without the preceeding 'KF-'.
    
    KF.py install <name>

**Example:**

    $ KF.py install ContainmentStation
    Installing KF-ContainmentStation

Disclaimer
----------
Whitelist maps and associated downloads scraped from sykosis.co.uk/kfmwhitelist/

All content is copyright their respective owners/authors.

The Installer is not affiliated with KFM Whitelist, Sykosis.

The Installer, KFM Whitelist, Sykosis are in no way related to nor affiliated with Tripwire Interactive, the Killing Floor game or map authors/creators.
