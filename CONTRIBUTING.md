# Contributing to the Project

This document details how you should contribute to this project, as a developer.

Should you wish to contribute to this project, please make sure you fulfil the [project prerequisites](#project-prerequisites), understand the [workflow](#project-workflow) behind this project, and follow the [procedure](#procedure-for-submitting-pull-requests) as described in this page.

## Contents

* [Project Prerequisites](#project-prerequisites)
* [Downloading the Project Files](#downloading-the-project-files)
* [Project Workflow](#project-workflow)
* [Procedure for Submitting Pull Requests](#procedure-for-submitting-pull-requests)
* [Follow-up Actions for Pull Requests](#follow-up-actions-for-pull-requests)
  * [Your pull request is approved](#your-pull-request-is-approved)
  * [Changes are requested for your pull request](#changes-are-requested-for-your-pull-request)
  * [Your pull request is rejected](#your-pull-request-is-rejected)
* [Issue Formats](#issue-formats)
  * [Issue: Bug](#issue-bug)
  * [Issue: Enhancement](#issue-enhancement)
* [List of Possible Contributions](#list-of-possible-contributions)
* [Other Queries](#other-queries)

## Project Prerequisites

***Project setup instructions will not be covered here. Please refer to [INSTALLING.md](https://github.com/nus-mtp/cs-modify/blob/master/INSTALLING.md) instead.***

This application was built on [`Python 2.7.12`](https://www.python.org/downloads/) using the [`web.py`](http://webpy.org/install) framework. This application is best viewed in [Google Chrome](https://www.google.com/chrome/) browser.

The following plugins are used for our project:
* Database: [`PostgreSQL`](https://www.postgresql.org/download/), [`psycopg2`](https://pypi.python.org/pypi/psycopg2) (The Python database adapter for PostgreSQL)

* Linting: [`pylint`](https://www.pylint.org/#install)

For linting, we abide largely to the [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/), with a few exceptions:

1. We use this convention for multiline comments:
```
'''
    This is the style for multi-line comments that we will adhere to.
    Note that there is a layer of indention after the first '''.
'''
```

2. We leave 2 newlines after the end of each function declaration.
```
def function_one():
    # do something


def function_two():
    # do another thing

# note the 2 newlines after the declaration of function_one()
```

* Testing: [`nose`](https://pypi.python.org/pypi/nose/1.3.7), [`paste`](https://pypi.python.org/pypi/Paste) (For UI testing)

To start contributing towards this project, **please ensure that you have these platforms/plugins installed on your machine**.

For continuous integration (CI) and deployment, we use the following platforms:

* CI: [`Travis CI`](https://travis-ci.org/)

* Deployment: [`Heroku`](https://www.heroku.com/)

## Downloading the Project Files

Our project files are located in the [CSModify repository](https://github.com/nus-mtp/cs-modify). You can either fork our repository to obtain the project files, or download the zip files from there.

## Project Workflow

We highly recommend that you abide by the project workflow as described here, for optimal development experience. However, it is absolutely not necessary to follow this workflow if it does not fit yours.

The project workflow is as follows:

1. Begin by writing test cases for the feature to be implemented.
  * If the feature to be implemented falls under a **back-end** component, the test cases should be written using the **`nose` API**.
  * If the feature to be implemented falls under a **front-end (UI)** component, the test cases should be written using **both the `nose` and `paste` API**.
  UI test cases should check that:
	* The expected HTML elements are present
	* The link navigations are functioning as expected (i.e. the user should be able to navigate successfully to any valid links present in the HTML page)
	* The form submissions in the page are working as intended. You should test accordingly for both valid and invalid input submissions.

2. Write codes to implement the feature(s).

3. Pylint both the code and your `nose` test cases.

4. Run your test cases and ensure that all your test cases pass.
    * In Windows, this can be done by running the command `nosetests`.
    * **If you are working in the Linux virtual environment that is set-up by `Vagrant`, you need to run the command `nosetests --exe` instead.**

5. Ensure that integration testing has passed (i.e. `Travis CI` reports that your code has passed).

6. If there are no problems in all of the above steps, create a pull request.

## Procedure for Submitting Pull Requests

1. Raise an issue in the issue tracker.
The issue raised should follow a specified [format](#issue-formats) (depending on the type of issue raised), which will be described in this page.

2. At this stage, linting and testing of your code should have been done.
If you need to ignore certain linting issues detected by `pylint`, please declare them in the pull request along with an explanation on why you did so.

3. Submit a pull request that references the issue you have raised.
Please note that the pull request should request for your code to be merged ***only*** with the `integration` branch. Any pull requests requesting to be merged with any other branch will be ***immediately rejected without review***.

    * We do not request for any specific format to be adhered to for pull requests, but please ensure that we can understand pretty much what you have implemented just from reading your pull request.

4. Wait for our feedback on your pull request.
You may need to wait for some period of time while we assign code reviewers to review your code. Please be patient during this period, we will update you of the status of your pull request when the review is complete.

## Follow-up Actions for Pull Requests

### Your pull request is approved

We will merge your pull request into the integration branch, and update the master repository accordingly. Thank you very much for contributing towards our project!

### Changes are requested for your pull request

We will need to discuss the changes requested with you on GitHub. We will leave the pull request open, but it will not be accepted for the time being, till the issues pertaining to it are resolved.

Should you not want to continue committing changes to the pull request, you may either close it yourself, or let us know so that we can close it for you.

### Your pull request is rejected

We will explicitly declare that your pull request is rejected. However, ***we will only close it 2 weeks later*** so as to provide you with a grace period, should you wish to justify why we should approve it.

If we do not hear from you after the grace period, the pull request will be closed and ***it shall not be reopened***.

Should you wish to reinstate the pull request (or any discussions pertaining to it), please submit another pull request instead.

## Issue Formats

There are 2 types of issues we will expect other developers to raise: a `bug` or an `enhancement`.

### Issue: Bug

The format for raising `bug` issues are as follows:

1. The `title` should be a short summary of the bug found

2. The `description` should contain the following:
  a) A detailed description of the bug
  b) What you expect to see (the expected outcome/result)
  c) What you actually observed (the actual outcome/result)
  d) The exact steps taken to result in the bug (accompanied by the relevant screenshots, if necessary)

3. Tag the issue with the `bug` label.

### Issue: Enhancement

The format for raising `enhancement` issues are as follows:

1. The `title` should be a short summary of what feature you wish to enhance/implement.

2. The `description` should contain the following:
  a) A detailed description of what feature you wish to enhance/implement
  b) Reason(s) for performing the above implementations

3. Tag the issue with the `enhancement` label.

## List of Possible Contributions

You may refer to the [Issue Tracker](https://github.com/nus-mtp/cs-modify/issues) or the [kanban board](https://github.com/nus-mtp/cs-modify/projects/1) to look out for things that you can contribute towards for this project.

Some of the possible contributions are listed here, for your convenience:

* Migrate UI test cases to [Selenium](http://www.seleniumhq.org/).
* Implement issue [#54](https://github.com/nus-mtp/cs-modify/issues/54) (Attach changelog message to modified-module feature).
* Implement a super-admin page for managing user accounts.
* Implement feature to have multiple alternative mounting plans accessible in the app.
* Implement feature of allowing module planners to upload mounting plans.
* Render module-prerequisite tree in the 'View Module' pages.
* Implement view of module-timeline showing the various AY-Semesters where students take prerequisite modules for a target module, before taking the target module in a specified AY-Semester.

## Other Queries

If you have any other queries on how to contribute to our project, you may contact us directly on GitHub, or drop us a mail at `nus-dot-csmodify-at-gmail-dot-com`.