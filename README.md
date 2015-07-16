# TumblRaider 2.1.5
a python script to download all images & videos from any tumblr.

<h3>Authors:</h3>
Danny Void & Aphects

<h3>Imports:</h3>
<code>os re sys json time urllib urllib2 urlparse argparse datetime</code>

<h3>Usage:</h3>
<pre>usage: TumblRaider.py [-h] -u tumblrusername [-r true/false] [-f foldertosavecontent] [-d 20]</pre>

<h3>Usage Arguments Explained:</h3>
<pre> -u tumblrUsernameHere [i.e. -u pybackup] [the tumblr username, excluding .tumblr.com]</pre>
<pre> -r true/false [optional] [download or skip reblogged content]</pre>
<pre> -f folderToSaveContent [optional] [name the folder you want content to be saved in]</pre>
<pre> -d integer [optional] [amount of duplicates found before you stop checking for new images]</pre>

<h3>Output:</h3>
<pre><code>$ python TumblRaider.py -u tumblrusername

TumblRaider 2.1.5
Authored By Danny Void & Aphects
-------------------------------
Looking up tumblrusername...
User found...
Looking through x total posts...
Found new content...
Downloading new content...
All done.
-------------------------------
</code></pre>

<h3>Where are the pictures?</h3>
All images are stored inside a newly created directory.<br />
<code>rips/tumblrusername/</code> if -r false<br />
<code>rips/tumblrusername/reblogs/</code> if -r true