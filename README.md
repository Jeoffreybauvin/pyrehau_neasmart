# py_rehau_neasmart

A python 3 package to interact with Rehaut Nea Smart interface

## What is Nea Smart Manager ?

If you are not familiar with the product "Nea Smart" from Rehau, this package won't be very useful for you ;).

Nea Smart Manager is an interface which allows you to control your Rehau electronic thermostat.

More informations here : https://www.rehau.com/en-en/nea-smart/english / https://www.rehau.com/download/1558632/nea-smart-manager-notice-d-installation-et-d-utilisation.pdf

Here is the interface provided by Rehau :

![neasmart_1](misc/images/neasmart_1.png)

![neasmart_2](misc/images/neasmart_2.png)

The problem : Nea Smart don't expose any public API. We need to play with Nea Smart interface. If you check at your web console, you'll see this : http://neasmart_ip/data/cyclic.xml. It's an XML file with all the informations you need. If you want to do some changes, you can post an XML form to /data/changes.xml.

Basically, this python package is a wrapper for this weird API :).
