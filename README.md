# flickr_backupr
Backup photos on Flickr

By default this will backup photos of you and photos you have favorited.
This will not backup your own photos. There are plenty of other tools out 
there that do that.

Required python packages:
* flickr_api
* six >=1.11

You'll also need [exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/) installed.

Steps:
1. python auth.py
1. python backup_photos.py
1. Go make a nice cocktail or two

It might fail on something. If so, let me know which image. 
You can then restart it and it should skip over everything 
it's already downloaded. If you're dealing with thousands of images
you'll have to be patient. This could probably be better optimized, but
I figure I'll only need to run it in its entirety once so :man_shrugging

Disclaimer: Not fully tested. YMMV. Please be nice to Flickr's API.
