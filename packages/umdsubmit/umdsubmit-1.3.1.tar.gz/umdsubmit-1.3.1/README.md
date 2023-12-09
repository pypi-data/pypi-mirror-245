# umdsubmit

This package allows submitting to the UMD Submit Server from the command line, without the Eclipse Plugin.

## Installation

You can install the package via pip:

```sh
pip install umdsubmit
```

## Usage
After installing navigate to the root of the project directory in the terminal and run the command umdsubmit. Enter your UMD Directory ID and password as requested. Ensure that you run the command from the directory containing the .submit file for the project.

## How It Works

1. **Initialization:**
   - The `umdsubmit` command is executed, initiating the submission process.

2. **Zip Archive Creation:**
   - The `shutil.make_archive` function is used to create a zip archive of the current working directory.

3. **File Reading - .submit:**
   - The `get_info` function is called to gather necessary submission data.
   - This function reads the `.submit` file in the current directory and retrieves values associated with specified keys.

4. **CVS Account Retrieval:**
   - The `get_cvs_account` function is called to obtain the CVS account.
   - If the `.submitUser` file exists, it is read to get the account information.
   - If the file doesn't exist, the `auth` function is triggered to authenticate the user.
  
5. **User Authentication (if needed):**
   - The `auth` function prompts the user to enter their UMD Directory ID and password.
   - A POST request is made to the server to negotiate a one-time password.
   - The server's response is written to the `.submitUser` file and printed to the console.

6. **One-Time Password Retrieval:**
   - The `get_one_time_password` function is called to retrieve a one-time password to authenticate with the submit server

7. **Submission:**
   - A POST request is made to the submit URL with the zip file and the gathered data.
   - The server's response is printed to the console.
