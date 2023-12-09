# Whiffle client

This client allows running atmospheric large-eddy simulations (LES) with Whiffle's GPU-resident model <https://whiffle.nl/>. 
The client requires an access token, which you can configure with the command line interface by executing,

`whiffle config edit user.token <your_token>`

You can create a new task by executing,

`whiffle task run <path_to_the_task_specification.[json|yaml]>`

The client polls the progress of the task until it has finished. The task will run in the background if you abort the client.
You can list the most recent tasks by executing,

`whiffle task list`

If you need an access token or you have any questions, please reach out to <support@whiffle.nl>.

## Command-line interface

### List the configuration

`whiffle config list`

### Change the token in the configuration

`whiffle config edit user.token <your_token>`

### Run a task

`whiffle task run <path_to_the_task_specification.[json|yaml]>`

### List tasks

`whiffle task list <number of tasks>`

### Download a task

`whiffle task download <task_id>`

### Attach a task

You can monitor the progress of a task and it will be automatically downloaded once the task has been successfully completed. 

`whiffle task attach <task_id>`