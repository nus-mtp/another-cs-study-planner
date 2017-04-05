# FAQ for Project Setup

We list down some ***commonly-encountered issues*** you might face while setting up our project, along with our suggested solutions.

Should you face an issue related to the project setup, that you are unable to solve, you can contact us on GitHub.

## Commonly Encountered Issues

1. Configuring `bootstrap.sh` and `local_database_data.py`?

    **Solution:**

  * In `bootstrap.sh`, set the `DB_PASSWORD` variable to be the password you use for your database.
    * If you are using a database that is not `postgres`, you have to manually declare a command in this script to create the database yourself.
  * In `local_database_data.py`, set the `database_name`, `user_name`, `password`, `host_name` and `port` that you use to connect to your database.


2. Encountering error `chown: changing ownership of /home/vagrant/csmodify: Not a directory` after running `vagrant up`

    **Solution:** Try reinstalling [VirtualBox](https://www.virtualbox.org/wiki/Downloads) again, then run `vagrant reload`.


3. Unable to run `vagrant ssh` in `cmd` (for Windows users)

    **Solution:** Set your PATH variable using the command `PATH=%PATH%;C:\Program Files\Git\usr\bin`. (**This assumes you already have Git Bash installed on your machine.**)


4. Encountering error `Stderr: VBoxManage.exe: error: VT-x is disabled in the BIOS for all CPU modes (VERR_VMX_MSR_ALL_VMX_DISABLED) VBoxManage.exe: error: Details: code E_FAIL (0x80004005), component ConsoleWrap, interface IConsole` after running `vagrant up`

    **Solution:** Please make sure that your machine supports virtualization.