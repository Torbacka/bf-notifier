# Getting an apartment in Stockholm

Getting an apartment from bostadsförmedlingen (bf) is a pain in the ass. After years and decades you'll probably get tired of hitting browser refresh button and would like to automate process as much as possible.

## Overview

This Python script checks if https://bostad.stockholm.se/ contains any new ads and notifies you via email.


All ads are being stored in a database.

### Dependencies

* Flask
* PyMysql
