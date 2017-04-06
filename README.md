

# IXP Remote Peering API

An API for remote peering metrics gathered from RIPE Atlas Probes.

## Getting started 

Clone the git repository, then run

    ./bin/venv_init

This will set up a virtual env and will install all
requirements.

It is recommeneded to install the additional packages
from `requirements-dev.txt` using

    ./bin/with_venv pip install -r requirements-dev.txt


## Initializing the database

Change the database configuration in `backend/settings.py` according
to your needs.

Then initialize the database by running

    ./bin/manage migrate


Afterwards you should start importing data.


## Importing data

Start with loading the **PeeringDB** IXP dataset by running:

    ./bin/manage ixp_import_peeringdb_ixps -f data/ix_peeringdb_data_20170405.txt

Now you are good to go and import the **remote interfaces** datafiles:

    ./bin/manage ixp_import_remote_interfaces -f data/remote_interfaces.AMS-IX.20160801.txt


**Optional:** After importing a remote interfaces dataset it is recommended
to resolve all member names from the imported ASNs.

You can do this by runnning

    ./bin/manage ixp_resolve_member_names

This will query PeeringDB by ASN and will fill in the
member names.

The PeeringDB queries are cached for 10 days.
The default cache directory is `/tmp/ixp_remote_peering_cache`. You 
can always change the cache location by editing the `CACHES` section
of `backend/settings.py`.





