# Python3 Command Line Interface for Twingate

A simple command line interface for Twingate in Python

## How to use it

1. Clone this repository
2. Install the required packages

```
pip install -r requirements.txt
```

3. Authenticate (you can pass a Session Name or let it generate one at random):

```
python ./tgcli.py auth login -t "my Twingate Tenant Name" -a "my Twingate API token"
```

3. Check CLI Help to look at available Commands:

```
python ./tgcli.py -h
```

4. Check CLI Help to look at available subcommands for a given command:

```
python ./tgcli.py auth -h
```

5. Check CLI Help to look at available parameters for a given subcommand:
```
python ./tgcli.py auth login -h
```

## Things to know:

Before you can run any of the commands, you need to **authenticate** using *python ./tgcli.py auth login*:

```
python ./tgcli.py auth login -t "my Twingate Tenant Name" -a "my Twingate API Token"
```

The **authentication token** along with the **Tenant Name** in the authentication call are **stored locally** and **do not need to be passed as parameters beyond the first authentication call**.

The **Session Name** needs to be passed in all calls (it serves to retrieve the Tenant name and Authentication Token dynamically)

Apart from the initial authentication call, each call should contain **at least 1 option**: **-s** (**-s** is used to specify the **Session Name**.)

The output format can be set to CSV, DF (DataFrame) or JSON (Default) by using the -f option in addition to the -s option


## Commands & Subcommands Currently Available:

* Twingate CLI:

  * auth
    * login: create a session
    * logout: revoke a session
    * list: list existing sessions

  * device
    * list
    * show
    * updateTrust
    * archive
    * block
    * unblock

  * dnssec
    * show
    * setAllowList
    * setDenyList
    
  * snumber (serial number)
    * list
    * add
    * remove

  * resource
    * list
    * show
    * create
    * delete
    * assignNetwork
    * visibility
    * address
    * alias

  * connector
    * list
    * show
    * create
    * rename
    * generateTokens
    * updateNotifications

  * group
    * list
    * show
    * addUsers
    * removeUsers
    * addResources
    * removeResources
    * create
    * delete
    * assignPolicy

  * user
    * list
    * show
    * role
    * create
    * delete
    * state

  * network
    * list
    * show
    * create
    * delete
  
  * policy
    * list
    * show
    * addGroups
    * removeGroups
    * setGroups

  * service account
    * list
    * show
    * create
    * delete
    * addResources 
    * removeResources

  * key
    * show
    * create
    * revoke
    * delete
    * rename
    

## Examples
```
# Authenticate
python ./tgcli.py auth login -t "my Twingate Tenant Name" -a "my Twingate API Token"
```

```
# List all devices (and display as Json (Default))
python ./tgcli.py -s RedPeacock device list
```

```
# List all devices (and display as DataFrame)
python ./tgcli.py -s RedPeacock -f DF device list
```

```
# List all devices (and display as CSV)
python ./tgcli.py -s RedPeacock -f CSV device list
```

```
# Update trust for a device (and set it to Trusted)
python ./tgcli.py -s RedPeacock device updateTrust -i "XXXabcNlOjE5MzI2OQ==" -t True
```

```
# Update trust for a list of devices (and set them to Untrusted)
python ./tgcli.py -s RedPeacock device updateTrust -l "XXXabcNlOjE5MzI2OQ==,YYYxyzFg4gT4SfC65K==" -t False
```
