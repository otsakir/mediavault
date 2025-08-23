
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
* 

