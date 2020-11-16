# Excavating-Occaneechi-Town

This project aims to modernize the "Excavating Occaneechi Town" website at
https://rla.unc.edu/dig by improving the website style, adding new features,
and simplifying the site structure.


## Getting Started
The project is intended to take very little tinkering to run. The steps are as
follows:
1. Obtain a copy of the old site, with exactly the same directory structure as
on the current site at https://rla.unc.edu/dig. Specifically, the site files
should all be contained in a directory called "dig", with a folder called
"html" inside the dig directory that contains the bulk of the rest of the site.
2. [Install Python 3.7+ from the official site](https://www.python.org/). Due
to the code's dependence on modules such as pathlib, **a version of 3.7 or later
is a hard requirement**.
3. Either download the code from this repo as a ZIP file (by clicking on the
green "Code" button near the top of the [repo home page]
(https://github.com/aychen99/Excavating-Occaneechi-Town/tree/master), or
[install Git](https://git-scm.com/downloads) and clone the repository to a
directory of your choosing through the command line by opening a command line
(for Windows) or a Terminal (for MacOS/Linux) and running the command  
`git clone https://github.com/aychen99/Excavating-Occaneechi-Town.git`  
in that directory.
4. Rename the "config_example.json" file in the root folder to "config.json",
or make a copy named "config.json". Change the value in quotes after
"digParentDirPath" to the directory where the old site files from step 1 were
saved to. For example, if the "dig" directory was saved in
"C:\Users\EOT\Old Site", so that the full path to the dig directory itself is
"C:\Users\EOT\Old Site\dig", then put "C:\Users\EOT\Old Site" as the value for
"digParentDirPath.
5. After ensuring that "config.json" has been updated properly in step 4,
although one can navigate on the command line/terminal to the folder
containing the repo, then run `pip install -r requirements.txt` and then
`python run_extraction_and_generation.py`, the process has also been simplified
so that Windows users can simply run "run_on_windows.bat" on a Windows machine,
or "run_on_mac_or_linux.sh" on a Mac OS X or Linux machine. As long as Python
3.7+ is installed and the config.json file has the proper location of the "dig"
directory, these scripts will automatically do the rest of the setup and then
run both extraction and generation.

The output will, by default, be stored in a folder called "newdig" in the same
main directory as the code itself. The intermediate JSON files generated will
be stored in a folder called "json" in the same main directory. The output
consists of static HTML files, where all the links are relative, and thus the
entire new site can "run" locally simply by opening up the static files in a
browser.

**Warranty**: These instructions were last tested by Andy (aychen99) on a
Windows 10 system on November 11, 2020.


## Testing
From the root directory (the one containing both the src and tests folders),
simply run `pytest` in the command line to run the tests in the tests folder.
To obtain a code coverage report, run
`coverage run --source=./src --omit ["./venv/*","./tests/*"] -m pytest` in the
root directory, then run `coverage html`, and open the "index.html" file in the
resulting "htmlcov" directory. If you've installed a Python venv in the current
directory, then the '--omit "./venv/*' is required for a proper coverage
report.


## Deployment
The project is very flexible in terms of where to generate the static HTML
files for the new site. The repository can be cloned to a local device, and
then as long as the user has access to the original site files and provides the
proper settings in the "config.json" file, the new site files will be generated
and written to the local device. The files may then be moved onto any server to
be hosted; there is no need for a particular type of backend, as long as it has
a couple gigabytes of free space and can serve static HTML files. As such, the
project also does not have any CI/CD enabled or use other addons, nor does it
have any staging or pre-production environments.

In practice, the final version of the site will be hosted according to the
decision of the UNC Professors who requested for this project to be done. It
will likely live on an official UNC server with set permissions, such that only
UNC ITS personnel or the Professors themselves may access it. Therefore,
deployment is best done by communicating with the professors/ITS, providing a
cloud storage drive (such as OneDrive or Google Drive) where any newly updated
site files will be stored, and requesting that they update the site files on
the hosting server whenever a change is made.

For testing purposes, as was done during the semester for this project, one can
also deploy the generated files to Netlify, or some other hosting service like
Heroku if desired. However, this would likely conflict with the actual site
hosted by UNC, so please seek permission before doing this.


## Technologies Used
The code in this repository uses the following technologies:
- Python 3.7+
- Beautiful Soup 4 library
- html5lib library (for use with Beautiful Soup)
- Jinja2 library
- pytest library
- coverage library
- Pillow library

The display of the final website, as well as features like navigation by page
number, depend on the following technologies:
- jQuery
- Bootstrap 4.5+
- [bootstrap-toc plugin](https://afeld.github.io/bootstrap-toc/)
- D3.js library

For architecture decision records on most of these technologies, see
[architecture_decision_records.md](./docs/architecture_decision_records.md) in
the "docs" folder.


## Contributing
Anyone is free to contribute to this project; contact aychen99 to be added as a
contributor and gain access to this repository. Additionally, meaningful
contribution to the project requires access to the original site files (the
"/dig" directory); contact Dr. Vin Steponaitis at UNC for access to those
files.

Source code is separated into two portions, an "extract_old_site" portion and a
"generate_new_site" portion, both stored in their own respective directories in
the "src" folder of the root folder. Tests are stored in a "tests" folder also
found in the root folder, and named "test_module_name.py" according to the
module name they are testing, with a subdirectory structure mirroring that of
the actual source code. Contributors should also follow this structure when
adding to the repository.

Documentation strings for functions and classes in this repository use numpy
docstring conventions. Other than that, adherence to PEP-8 or general
"Pythonic" style conventions should do.

You can also visit the [COMP 523 class site](https://tarheels.live/comp523eot/)
for this project for more information.


## Authors
- Jacob King (jmking628)
- Andy Chen (aychen99)
- Ankush Vij (vijankush)


## License
This project is licensed under the terms of the MIT license.


## Acknowledgements
Special thanks to Drs. Vin Steponaitis and R.P. Stephen Davis for their
continued support and enthusiasm for this project, and to our COMP 523 mentor
for helping guide us through this project and for providing invaluable
technical assistance. Also, thanks to Mike Bostock (creator of D3.js) for his
work on  [this demo](https://observablehq.com/@d3/zoom-to-bounding-box), which
was instrumental for the creation of this project's excavation map.
