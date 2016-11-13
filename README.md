# Tumblrchive 3.0.0
a python script to download all images & videos from any tumblr.

<h3>Usage:</h3>
<pre>usage: Tumblrchive.py [-h] -u tumblrusername [-r true/false] [-f folderToSaveContent] [-d 20]</pre>

<h3>Usage Arguments Explained:</h3>
<pre> -u tumblrUsernameHere [i.e. -u pybackup] [the tumblr username, excluding .tumblr.com]</pre>
<pre> -r true/false [optional] [download or skip reblogged content]</pre>
<pre> -f folderToSaveContent [optional] [name the folder you want content to be saved in]</pre>
<pre> -d integer [optional] [amount of duplicates found before you stop checking for new images]</pre>

<h3>Output:</h3>
<pre><code>$ python TumblRaider.py -u tumblrusername

Tumblrchive 3.0.0
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
<code>rips/tumblrusername/Tumblr/</code> if -r false<br />
<code>rips/tumblrusername/Tumblr/reblogs/</code> if -r true
