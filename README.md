
## Security

The following permissions seem appropriate:

* **Bucket guests** - Users that can only read the contents of a single bucket. They can download, or view stuff. They can't alter it. Also
  it makes sense to time-limit their access. `content.download_contentitem`, `content.view_contentitem`
* **Bucket moderators** - Users that can add/remove content to the bucket or modify content items name and other fields. They won't be able to alter the settings of a bucket. They should play by 
  the rules. `content.add_contentitem`, `content.delete_contentitem`, `content.change_contentitem`
* **Bucket Admins** - Users that can administer a bucket. That is, change its settings, invite people to use it or even 
  delete the bucket. `content.add_bucket`, `content.delete_bucket`, `content.change_bucket`
  TODO: add permission strings
* **Instance Admins** - Users than can create new buckets.

Each of the behaviors above will be implemented as a permission. 

The following roles seem appropriate:

* **Bucket user** - Bucket users have access to a single bucket. They can download and view and push new content to it.
  They can't create other buckets.
* **Bucket guest** - Same as Bucket user but in a read-only fashion.

## Dependencies

ffmpeg, ffprobe, youtube-dl


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

