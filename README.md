# tRaidr 1.1.8
a python script to download all images from any tumblr.

<h3>Authors:</h3>
Aphects & DannyVoid

<h3>Dependencies:</h3>
<code>os re sys json time urllib urllib2 urlparse argparse datetime</code>

<h3>Usage:</h3>
<pre>usage: tRaidr.py [-h] -u tumblrusername [-r true/false] [-f foldertosavecontent] [-d 20]</pre>

<h3>Usage Arguments Explained:</h3>
<pre> -u tumblrUsernameHere [i.e. -u pybackup] [the tumblr username, excluding .tumblr.com]</pre>
<pre> -r true [optional] [downloads reblogged content only]</pre>
<pre> -r false [optional] [downloads unique, non-reblogged content only]</pre>
<pre> -f folderToSaveContent [optional] [name the folder you want content to be saved in]</pre>
<pre> -d integer [optional] [amount of duplicates found before you stop checking for new images]</pre>

<h3>Output:</h3>
<pre><code>$ python tRaidr.py -u tumblrusername -r false

tRaidr 1.1.8
Authored By Aphects & DannyVoid
-------------------------------
Looking up tumblrusername...
User found...
Looking through x total posts...
Found new images...
Downloading images...
All done.
-------------------------------
</code></pre>

<h3>Where are the pictures?</h3>
All images are stored inside a newly created directory.<br />
<code>rips/tumblrusername/</code> if -r false<br />
<code>rips/tumblrusername/reblogs/</code> if -r true

<h3>Coming Soon:</h3>
Add the option to download ALL unique, non-reblogged videos.<br />
Replace urlretrieve with urllib2 to add user-agents to all requests.<br />
Create an executable for people who can't, or don't know how to run python.<br />
<s>Add argument to download ALL images, not just unique, non-reblogged content.</s><br />
<s>Option to leave the <code>foldertosaveimages</code> argument blank, and just default to <code>tumblrusername</code>.</s><br />
<s>Create a log file to log usage, for your future refrence..</s><br />