[![Build Status](https://github.com/csyezheng/coursera-helper/workflows/Run%20Unit%20Tests/badge.svg)](https://github.com/csyezheng/coursera-helper/actions/workflows/)
[![Coverage Status](https://coveralls.io/repos/csyezheng/coursera-helper/badge.svg)](https://coveralls.io/r/coursera-helper/coursera-helper)
[![Code Climate](https://codeclimate.com/github/csyezheng/coursera-helper/badges/gpa.svg)](https://codeclimate.com/github/csyezheng/coursera-helper)
[![Latest version on PyPI](https://img.shields.io/pypi/v/coursera-helper.svg)](https://pypi.python.org/pypi/coursera-helper)

# coursera-helper

`coursera-helper` is forked from [coursera-dl](https://github.com/coursera-dl/coursera-dl) which is no longer maintained.

<!-- TOC -->

  * [Introduction](#introduction)
  * [Installation instructions](#installation-instructions)
    + [Installation (recommended)](#installation-recommended)
    + [Manual Installation](#manual-installation)
    + [Docker container](#docker-container)
  * [Before the start](#before-the-start)
  * [Quick Start](#quick-start)
    + [List courses](#list-courses)
    + [Download course](#download-course)
    + [More download options](#more-download-options)
    + [Use configuration file](#use-configuration-file)
  * [Troubleshooting](#troubleshooting)
    + [china-issues](#china-issues)
  * [Reporting issues](#reporting-issues)
  * [Disclaimer](#disclaimer)

  <!-- /TOC -->

## Introduction

`coursera-helper` is a tool for downloading Coursera.org videos and naming them..  

It is platform independent, and should work fine under Unix (Linux, BSDs etc.), Windows or Mac OS X.

## Installation instructions

`coursera-helper` requires Python 3 and very few other dependencies. (As of October 2023, `coursera-helper` passed the test of Python versions 3.8, 3.9, 3.10, and 3.11).

### Installation (recommended)

Opening a terminal and typing the command If you have installed Python:

    pip install coursera-helper

### Manual Installation

    pip install git+https://github.com/csyezheng/coursera-helper.git

### Docker container

You can run this application via [Docker](https://docker.com) if you want. Just install docker and run

```
docker run --rm -it -v \
    "$(pwd):/courses" \
     csyezheng/coursera-helper --cauth <CAUTH-value> <course name>
```

* Please note that it will prompt that unable to find the image locally, please wait patiently for downloading.
* **Please note that** when running in docker mode, only the `--cauth` parameter can be passed for authentication, and username, password, and `--browser-cookie` parameters are not accepted.

* The course files will be downloaded to your current directory.

## Before the start

`coursera-helper` supports four authentication methods:

1. **CAUTH (recommended)**

   Just use the `--cauth CAUTH-value-from-browser` option when running the program.

   [How to get the cauth value?](#CAUTH)

2. Browser cookies

   Just use the `--browser-cookie` option when running the program.

   Automatically extract CAUTH value from the browser cookie. If this method fails, please use other authentication methods.

3. Username and Password

   Just use the `-u <user> -p <pass>` options when running the program.

   Please note that this method will open the browser, you may have to click on the reCAPTCHA.

4. netrc File

   Just use the `--netrc` options when running the program.

## Quick Start

Run the following command to query the usage and options:

```
coursera-helper --help
```

### List courses

Run the following command to query the courses in which you are enrolled:

```
coursera-helper --cauth <CAUTH> --list-courses
```

or

```
coursera-helper --browser-cookie --list-courses
```

or

    coursera-helper -u <email or username> --list-courses

### Download course

From there, choose the course you are interested in, copy its course name and use it
in the following command:

    coursera-helper -u <email or username> <COURSE NAME>

Your downloaded videos will be placed in current directory, but you can also choose another destination with the `--path` argument.


### More download options

General download:

```
coursera-helper --cauth <CAUTH> <COURSE NAME>
```

Specify download location:

```
coursera-helper --cauth <CAUTH> --path <PATH> <COURSE NAME>
```

Download with subtitles:

```
coursera-helper --cauth <CAUTH> --subtitle-language en,zh-CN|zh-TW <COURSE NAME>
```

Specify video resolution：

```
coursera-helper --cauth <CAUTH> --video-resolution 720p <COURSE NAME>
```

Download with quizzes:

```
coursera-helper --cauth <CAUTH> --download-quizzes <COURSE NAME>
```

Download with notebooks:

```
coursera-helper --cauth <CAUTH> --download-notebooks <COURSE NAME>
```

### Use configuration file

Alternatively, if you want to store your preferred parameters (which might also include your username and password), create a file named `coursera-dl.conf` where the script is supposed to be executed, with the following format:

```
--username <user>
--password <pass>
--subtitle-language en,zh-CN|zh-TW
--download-quizzes
--download-notebooks
--video-resolution 720p
--download-delay 10
--cauth <cauth value>
```

If you have created a file named `coursera-dl.conf`, you just download course with command:

```
coursera-helper <COURSE NAME>
```

## Troubleshooting

### CAUTH

Find your coursera CAUTH:

* Open and login to https://www.coursera.org/
* Right-click on the touchpad or mouse until you find *inspect*.
* Go to Applications > Cookies (and click dropdown) > click https://www.coursera.org/ > find and click CAUTH > Copy value CAUTH.

**Chrome**:

1. Open the browser and login to https://www.coursera.org/

2. Open the last DevTools panel

   Windows or Linux: Press **F12** on the keyboard. Or press the **Ctrl** + **Shift** + **I** keys.

   Mac: Press **Fn** + **F12** on the keyboard. Or press the **Cmd** + **Option** + **I** keys.

3. Open **Application** > **Storage** > **Cookies** and select https://www.coursera.org/.

4. find and click CAUTH > Copy value CAUTH

**Firefox**:

1. Open the browser and login to https://www.coursera.org/

2. Open the last DevTools panel

   Windows or Linux: Press **F12** on the keyboard. Or press the **Ctrl** + **Shift** + **I** keys.

   Mac: Press **Fn** + **F12** on the keyboard. Or press the **Cmd** + **Option** + **I** keys.

3. Open **Storage** > **Cookies** and select https://www.coursera.org/.

4. find and click CAUTH > Copy value CAUTH

### china-issues

If you are from China and you're having problems downloading videos, adding 

```
52.84.167.78   d3c33hcgiwev3.cloudfront.net
```

in the hosts file (`/etc/hosts` or `C:\Windows\System32\drivers\etc`) 

Flush DNS with this command in the terminal.

```
ipconfig /flushdns
```

## Reporting issues

Before reporting any issue please follow the steps below:

1. Verify that you are running the latest version of all the programs.  Use the following command if in doubt:

        pip install --upgrade coursera-helper
   
3. If the problem persists, feel free to [open an issue](https://github.com/csyezheng/coursera-helper/issues) in our bug tracker, please fill the issue template with *as much information as
possible*.

## Disclaimer

`coursera-helper` is meant to be used only for your material that coursera gives you access to download. We do not encourage any use that violates their Terms Of Use.

