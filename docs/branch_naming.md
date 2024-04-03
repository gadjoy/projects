# Branch Naming
Git branch naming policy for Gadjoy Team

## Format
Git branch names **MUST** follow one of the following formats
- user_name/project_name/component_name/purpose

   examples:  `aditya/venus/qch/dev`, `vivek/venus/qch/test`
- project_name/component_name/release-major.minor.patch

   example: `europa/devops/release-1.2.3`
- project_name/release-major.minor.patch

   example: `europa/release-1.2.3`

## Naming Units
- project: europa, venus, jupiter
- component: uploader, qch, devops, reader, signaling
- purpose: dev, test, integration, build, release-major.minor.version
- user_name: srinivas, asutosh, vivek, aditya


## Command Line


**Create New Branch from Old Branch**

`$ git checkout <old_name>`

`$ git branch -m <new_name>`

`$ git push origin -u <new_name>`

`$ git push origin --delete <old_name>`

**Delete Branch, if not done already**

`$ git push origin --delete <old_name>`
