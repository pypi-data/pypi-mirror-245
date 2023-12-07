# VirtualCollegeAPI

original API DOCS  https://enableapi.docs.apiary.io/#reference/security/access-tokens

This is a small project, the entire API is not covered yet, 
I just added the methods that I needed, PRs are welcome.

it handles the creation of JWT and the encoding


## Install
`pip install virtualcollegeapiwrapper`

## Usage example
```
from VirtualCollegeAPIWrapper.VirtualCollege import VirtualCollegeAPI

# InstanceReference and PublicKeyAPI can be found in Virtual college -> Settings -> Api Settings
# You will need an admin account

VC = VirtualCollegeAPI(InstanceReference, PublicKeyAPI, "https://external-api.vc-enable.co.uk")
print(VC.count_users())
```

For the list of methods look at the Class VirtualCollegeAPI code.