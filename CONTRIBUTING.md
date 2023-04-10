# Contribution Guidelines

## Table of contents

* [Contribution Guidelines](#contribution-guidelines)
  * [Table of contents](#table-of-contents)
  * [Style conventions](#style-conventions)
    * [Code style (PEP 8)](#code-style-pep-8)
    * [Docstrings (NumPy)](#docstrings-numpy)
  * [Unit testing](#unit-testing)
    * [What should be tested?](#what-should-be-tested)
  * [Pull Requests (PR)](#pull-requests-pr)
    * [Reviewing a Pull Request](#reviewing-a-pull-request)
    * [Your First Contribution](#your-first-contribution)

## Style conventions

### Code style (PEP 8)

To keep our code consistent and ease collaboration, we all follow the PEP 8 style convention. You can read about PEP 8 [here](https://peps.python.org/pep-0008/). Please take a look and familiarise yourself with these conventions. Some examples of what this style uses are:

* Use 4 spaces per indentation level
* Limit all lines to a maximum of 88 characters
* Imports are always put at the top of the file and are grouped by type.
* Class names should normally use the CapWords convention
* Function and variable names should be lowercase, with words separated by underscores as necessary to improve readability
* (Many more recommendations)

The style of our code will be continuously checked via pylint when you submit a Pull Request to merge code to branch `master`. Any inconsistency will be flagged and will block the pull request until it is resolved. It's recommended to set up your IDE to automatically enforce  PEP 8 style. For instance, PyCharm can automatically reformat your code to be PEP 8 compliant (see [here](https://www.jetbrains.com/help/pycharm/reformat-and-rearrange-code.html)).

### Docstrings (NumPy)

For docstrings we'll rely on the NumPy style described [here](https://numpydoc.readthedocs.io/en/latest/format.html). Your IDE is also able to automatically populate docstrings in our style of choice, so it's a good idea to configure this too (see this [example in PyCharm](https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html)).

## Unit testing

We'll need critical components of our code in branches `prod` and  `prod_stable` tested. If you are not familiar with unit testing the following introduction is a good place to start: [Introduction to unit testing](https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/).

Our code will be continuously tested via pytest when you submit a Pull Request to merge code to branches `prod` and `prod_stable`. Any failing test will be flagged and will block the pull request until it is resolved.

### What should be tested?

This depends. Ideally, all code is tested so it can be proven to be bug free, but writing tests takes time and this is not practical. In practice, this is a trade-off between speed of development and code reliability. When contributing your code, components that are good candidates for testing are:

1. Used repeatedly
2. Foundational for other components, or support other processing
3. Likely to be reused by colleagues

A good example of the above could be a code component that simulates the undersampling of raw ultra-sound data. If this component contains a bug, any conclusions derived from it will be inaccurate and this would be very costly.

Code elements that generally won't require testing could be notebooks or scripts used to extract and plot results as a one-off process, or processes derived almost directly from third-party libraries (which are themselves usually tested).

## Pull Requests (PR)

We're following a Git workflow to collaborate at scale and efficiently. If you're not familiar with Git a good starting point would be to read tutorials such as [this one](https://nvie.com/posts/a-successful-git-branching-model/) or these from Atlassian ([tutorial 1](https://www.atlassian.com/git/tutorials/comparing-workflows#:~:text=A%20Git%20workflow%20is%20a,in%20how%20users%20manage%20changes.), [tutorial 2](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)).

We'll be using a simplified version of the workflows described in the tutorials above. In its simplest form, our repository will contain three types of branches:

* `prod_stable` branch: This contains the most stable version of our code. Unit tests should always pass in this branch.
* `prod` branch: This contains a stable version of our code which is derived from `prod_stable`. It is intended to be used for all intermediate versions of our code. Unit tests should always pass in this branch.
* `staging` branches: This represents an intermediate branch from which new features are implemented and it is derived from `prod` branch. It is mainly used to receive new features and tests them before merging them in the `prod` through a Pull Request.
* `feature` branches: Feature branches are derived from `staging` and are intended for the development of features, so we don't expect them to be tested and reliable at all times. Once the feature is finalized, we'll test core components it brings into the code and merge it into `staging` through a Pull Request.

### Reviewing a Pull Request

Anyone can review pull requests, we encourage others to review each other's work, however, only the maintainers can
approve a pull request. Pull Requests require at least one approval and all tests passing before being able to merge it.

### Your First Contribution

Working on your first Pull Request? You can learn how from this _free_series, [How to Contribute to an Open Source Project on GitHub](https://app.egghead.io/playlists/how-to-contribute-to-an-open-source-project-on-github). If you prefer to read through some tutorials, visit <https://makeapullrequest.com/> and <https://www.firsttimersonly.com/>

At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first :relaxed:
