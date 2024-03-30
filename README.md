# Setup

* WSL-Python - docs/wsl_python.md
* Github - docs/github_setup.md
* [Virtual-Env-Python](docs/virutal_environment_setup.md)
* AI-Pair-AWS - docs/aws_codewhisperer_setup.md
* [Server-Python-Flask](/docs/server_setup.md)
* [Client-JS-Vue](docs/Client_setup.md)

# Golden Configuration as March-26-2024

Please use the below versions for optimal use and easy setup. This would be updated to the latest stable build continously. Check these version before you start troubleshooting.

|Software	| Version |
| --------- | ------- |
| Ubuntu	| 20.04 |
| python*	| 3.10.13 |
| VSCode	| 1.87.2 |
| node*    | 18.3.0 |
| npm | 8.11.0 |
| nvm | 0.39.1 |

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
