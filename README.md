# AWS IAM Identity Center User and Group API Operations

This project provides examples and sample code to manage and audit AWS IAM identity store User and Group operations at scale using APIs. With these APIs, you can build automation workflows to:
* Provision and de-provision users and groups 
* Add new members to a group or remove them from a group
* Query information about users and groups in IAM Identity Center
* Update information about these users and groups
* Find out which users are members of which groups

## Prerequisites

Before you start you should have the following prerequisites:
  * An Organization in AWS Organizations
  * Administrative access to the AWS IAM Identity Center
  * Python version 3.10.5 or later
  * AWS CLI

## Environment Setup

Clone this repo:

```
git clone https://github.com/aws-samples/iam-identitycenter-identitystoreapi-operations

```

## Test `identitystore_operations.py`

Here is an example to see all supported operations available in the sample script.

```
python identitystore_operations.py —h

*Sample Output:*
usage: identitystore_operations.py [-h]
                                   {create_user,create_group,adduser_to_group,delete_group,list_members,list_membership}
                                   ...
positional arguments:
  {create_user,create_group,adduser_to_group,delete_group,list_members,list_membership}

options:
  -h, --help            show this help message and exit

```

## AWS IAM Identity Center User and Group API Operations

Here is an example of how you can create a new user “John Doe” in the IAM Identity Center identity store and add the user to an existing “AWS_Data_Science” Group.

```
python identitystore_operations.py create_user --identitystoreid d-123456a7890 --username johndoe --givenname John --familyname Doe --groupname AWS_SSO_Data_Science

*Sample Output:*
User:johndoe with UserId:94482488-3041-7026-18f3-be45837cd0e4 created successfully
User:johndoe added to Group:AWS_Data_Science successfully
```

Now, consider the data scientist transitions to an applied scientist role and needs access to additional AWS applications and resources. Previously, you had to manually update their information and add them to the “AWS_Applied_Scientists” group so they get the right access. Now, your automation can update the user and provide them with the access they need. 
 
Here is an example of how a previously created user “John Doe” can be added to“AWS_Applied_Scientists” group

```
python identitystore_operations.py adduser_to_group --identitystoreid d-123456a7890 --groupname AWS_SSO_Applied_Scientists --username johndoe

*Sample Output:*
User:johndoe added to Group:AWS_Applied_Scientists successfully
```

## AWS IAM Identity Center User and Group Audit Operations

Here is an example of how you can find all members of “AWS_Applied_Scientists” group

```
python identitystore_operations.py list_members --identitystoreid d-123456a7890 --groupname AWS_SSO_Applied_Scientists 

*Sample Output:*
UserName:johndoe,Display Name: John Doe 
```

Here is an example of how you can find group memberships of a specific user “johndoe”

```
python identitystore_operations.py list_membership --identitystoreid d-123456a7890 --username johndoe

*Sample Output*
User :johndoe is a member of the following groups
AWS_Data_Science
AWS_Applied_Scientists
```

## Test `identitystore_bulkoperations.py`

Here is an example to see all supported bulk operations available in the sample script.

```
python identitystore_bulkoperations.py —h

*Sample Output:*
usage: identitystore_bulkoperations.py [-h] {create_users,delete_users} ...

positional arguments:
  {create_users,delete_users}

options:
  -h, --help            show this help message and exit

```

## AWS IAM Identity Center Bulk Operations

Here is an example of how you can bulk create new users from a CSV file and add the user to an existing “AWS_Data_Science” Group.

First prepare a csv file with your identities as in [example csv file](examples/example.csv) with the required fields:

```
username,givenname,familyname,groupname,email,emailtype,primary
nina_franco,Nina,Franco,AWS_SSO_Data_Science,nina.franco@world.universe,work,TRUE
john_smith,John,Smith,AWS_SSO_Data_Science,john.smith@world.universe,work,TRUE
```

The API supports creating with emails, which the script assumes are present in the CSV file.
However the API does not yet support automatically sending verification emails.
Once users are created you will need to go to the console and send the verification emails.

Identity store allows you to specify multiple emails for each user.
The example script enables you to specify a single email per user.
The email type is a string, in the example defaulting to `work`, while primary is a binary field and must be `TRUE` or `FALSE`.
If you want to use the email to verify users, ensure primary is `TRUE`.

```
python identitystore_bulkoperations.py create_users --identitystoreid d-123456a7890 --identities_file IDENTITIES.csv

*Sample Output:*
User:nina_franco with UserId:12345678-3041-7026-18f3-be45837cd0e4 created successfully
User:nina_franco added to Group:AWS_Data_Science successfully
User:john_smith with UserId:94482488-3041-7026-18f3-be45837cd0e4 created successfully
User:john_smith added to Group:AWS_Data_Science successfully
```

The `delete_users` example can be used to delete users, using the same IDENTITIES.csv, though this only requires, the usernames.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

