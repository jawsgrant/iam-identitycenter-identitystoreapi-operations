#Python program for AWS Identity bulk User Management

# CSV format for identities to be created:
# username,givenname,familyname,groupname,email,emailtype,primary
# nina_franco,Nina,Franco,ExistingGroup,nina.franco@world.universse,work,TRUE
# ...

import argparse
import json
import boto3
import csv

client = boto3.client('identitystore')

def create_users(args):
    """ 
    This function creates bulks user and adds each user to groups if the group exists.
    - If the group does not exists , this function will create only the user and skip adding user to the group
    
    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    
    --identitystoreid - Identity Store Id of SSO configuration
    --identities_file - CSV file containing identities:
    
    Required fields
    -------------------

    username  - User Name for the user
    givenname - First Name for the user
    familyname - Last Name for the user
    groupname - Name of the SSO group !! Only accepts a single groupname
    email - Email !! Only accepts a single email
    email_type - Type of email, e.g. work, personal
    primary - Binary True|False
 
    Response
    --------
    None


    """

    sso_id_storeid = args.identitystoreid
    ids_filename = args.identities_file

    try:
        with open(ids_filename, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            rows=[]
            for row in reader:
                rows.append(row)
                print(row)

    except:
        raise Exception('Unable to parse specified file: %s. Check file exists and verify file format' % ids_filename)

    for row in rows:
        user_name = row['username']
        given_name = row['givenname']
        family_name = row['familyname']
        display_name = "{} {}".format(given_name, family_name)

        groupnameFlag=False
        if 'groupname' in row:
            groupnameFlag=True
            group_name = row['groupname']
        
        emailFlag=False
        if 'email' in row:
            emailFlag=True
            email=row['email']
            email_type=row['emailtype']
            if row['primary']=='TRUE':
                primary=True
            elif row['Primary']=='FALSE':
                primary=False
            else:
                raise Exception('Email provided for %s but primary neither True nor False' % user_name)

        user_payload = {}
        user_payload['IdentityStoreId']=sso_id_storeid
        user_payload['UserName'] = user_name
        user_payload['DisplayName'] = display_name
        user_payload['Name']={
                'FamilyName': family_name,
                'GivenName': given_name            
        }
        if emailFlag:
            user_payload['Emails']=[{'Value': email, 'Type': email_type, 'Primary': primary}]

        print(user_payload)
        create_user_response = client.create_user(**user_payload)

        user_id = create_user_response["UserId"]
        
        print("User:{} with UserId:{} created successfully".format(
            user_name, create_user_response["UserId"]))
        group_exists = True
        if groupnameFlag:
            try:
                get_group_id_response = client.get_group_id(
                    AlternateIdentifier={
                        'UniqueAttribute': {
                            'AttributePath': 'displayName',
                            'AttributeValue': group_name
                        }
                    },
                    IdentityStoreId=sso_id_storeid
                )
            except client.exceptions.ResourceNotFoundException as e:
                print("Group Name {} does not exists, Skipping adding user to group".format(
                    group_name))
                group_exists = False
        if group_exists:
            create_group_membership_response = client.create_group_membership(
                GroupId=(get_group_id_response["GroupId"]),
                IdentityStoreId=sso_id_storeid,
                MemberId={
                    'UserId': user_id
                }
            )
            
            print("User:{} added to Group:{} successfully".format(
                user_name, group_name))

def delete_users(args):
    """ 
    This function deletes bulks user and adds each user to groups if the group exists.
    - If the group does not exists , this function will delete only the user and skip adding user to the group
    
    Note: Uses the region set in the default profile or shell environment
    
    Required parameters
    -------------------
    
    --identitystoreid - Identity Store Id of SSO configuration
    --identities_file - CSV file containing identities:
    
    Required fields
    -------------------

    username  - User Name for the user
 
    Response
    --------
    None


    """

    sso_id_storeid = args.identitystoreid
    ids_filename = args.identities_file

    try:
        with open(ids_filename, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            rows=[]
            for row in reader:
                rows.append(row)
                print(row)

    except:
        raise Exception('Unable to parse specified file: %s. Check file exists and verify file format' % ids_filename)

    for row in rows:
        user_name = row['username']

        user_id=client.get_user_id(
            IdentityStoreId=sso_id_storeid,
            AlternateIdentifier={
                'UniqueAttribute': {
                'AttributePath': 'UserName',
                'AttributeValue': user_name
                }
            }
        )['UserId']

        client.delete_user(
            IdentityStoreId=sso_id_storeid,
            UserId=user_id)
        

        print("User:{} with UserId:{} deleted successfully".format(
            user_name, user_id))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    #sub-parsers for creating multiple users in IAM Identity Store
    create_users_parser = subparsers.add_parser('create_users')
    create_users_parser.add_argument(
        '--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    create_users_parser.add_argument(
        '--identities_file', required=True, help="Filename for csv file with identities to be added")
    create_users_parser.set_defaults(func=create_users)

    #sub-parsers for deleting multiple users in IAM Identity Store
    delete_users_parser = subparsers.add_parser('delete_users')
    delete_users_parser.add_argument(
        '--identitystoreid', required=True, help="Identity Store Id for IAM Identity Center Directory Configuration")
    delete_users_parser.add_argument(
        '--identities_file', required=True, help="Filename for csv file with identities to be added")
    delete_users_parser.set_defaults(func=delete_users)

    args = parser.parse_args()
    args.func(args)
