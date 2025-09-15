
## Security

There are two kinds of permissions used. 
* `user permissions`. They grant access to the user performing operations like "see the list of 
buckets" or "create new buckets". Such permissions are implemented using the built-in django permission mechanism. 
Generic views are secured using the `PermissionRequiredMixin` and respective `permission_required` attribute. 
* `bucket permissions`. Those that grant a user access of some type to specific bucket objects. For example,
'edit the details of a bucket'. These permissions are implemented using a custom permission mechanism (see core/security.py)
and are stored in the BucketPermissions database model. To guard a generic view with these type of permissions extend 
`AuthorizeBucketAccessMixin` and add the following property to the view class:

    bucket_permission_set = [Permissions.edit_details]


### `user permissions`

* `buckets.view_bucket`. User is allowed to access the bucket list view. In any case, he will see only the buckets that
  are related to him through BucketPermission objects.
* `buckets.add_bucket`. User can create new buckets.


### `bucket permissions`

* view = 0
* edit_details = 1
* remove = 2
* add_content = 3
* remove_content = 4
* play_content = 5
* download_content = 6
* view_tasks = 7
* update_tasks = 8
* modify_permissions = 9
* manage_users = 10


### Internals

Internally, bucket permissions are represented as a string of size 30 characters. Each position in the string corresponds to a specific
permission. For example, at index 0 we have 'READ_ACCESS'. A permission character can have one of the following values:

. : The permission is not set. It may not be defined or it may not be set. Initially, all indexes will be undefined. 
T : The permission is set.
F : The permission is negative. We'll see if this makes sense and how it will be different from '.'


### Roles

Conceptually the following roles seem appropriate:

* **Bucket guests** - Users that can only read the contents of a single bucket. They can download, or view stuff. They can't alter it. Also
  it makes sense to time-limit their access.
* **Bucket moderators** - Users that can add/remove content to the bucket or modify content items name and other fields. They won't be able to alter the settings of a bucket. They should play by 
  the rules.
* **Bucket Admins** - Users that can administer a bucket. That is, change its settings, invite people to use it or even 
  delete the bucket.
* **Instance Admins** - Users than can create new buckets.

Each of the behaviors above will be implemented in terms of _bucket permissions_. 


## Dependencies

ffmpeg, ffprobe, youtube-dl


## Django apps

**Buckets**. Bucket CRUD. Per-bucket user permissions. Async task overview. Relation to community. 

**Content**. Bucket content. ContentItem CRUD. Content upload tasks. Content download, streaming and media player.

**Community**. We have community models. Each community may have members. Add members to a cummunity. Invitations.

**Core**. TBD.


## Data schema

* A user might be a member of a single community. Membership is signified by the existence of a Member entity attached to 
  the user object. The Member attached object has a required foreign key to the Community. You can further get the members
  of a community by accessing community.member_set property.
* The actual benefits members of a community will enjoy is a thing to define. For now, it's just a list of members that
  are offered as suggested users to gain access to a bucket.
* Initially a user belongs to no community. He can then start a community. That means create a community object and 
  attach himself a Member object for that community. 
* Adding access to a bucket involves adding users to its 'users' property. The suggested users to pick from will be the 
  members of a community. 


### Views

* Bucket users. Have a textbox for the user to add new members to the bucket. Show that in the Bucket/1/users.

* `POST community/` .Create a community for the current user if he doesn't already have one. Give a 'name'.
* Invite members to the community. Or we might as well add them with no questions asked.

