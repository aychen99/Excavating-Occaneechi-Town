from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import pathlib
import modules.text_classes as tc


def generate_chapters(chapters_dir):
    """
    Define the structure of the site's text chapters for sidebar.
    Populates a list, 'chapters', with the basic chapter structure information
    required to generate page sidebars.
    Parameters
    ----------
    chapters_dir : str
        Pathlike string containing the path to the directory with the chapter
        data files.
    Returns
    -------
    chapters : List of 'Chapter' objects
        List of 'Chapter' objects, each decorated with all of the old site data
        for that chapter.
    """

    chapters = []

    # TODO: reconsider chapter structure hardcoding
    # TODO: settle how we name hrefs, placeholders for now, most replaced below
    chapter_names_links = [
        ("Getting Started", "001_getting_started.html"),
        ("Archaeology Primer", "002_archaeology_primer.html"),
        ("Introduction", "01_introduction.html"),
        ("Contents", "02_contents.html"),
        ("Background", "1_background.html"),
        ("Excavations", "2_excavations.html"),
        ("Artifacts", "3_artifacts.html"),
        ("Food Remains", "4_food_remains.html"),
        ("Interpretations", "5_interpretations.html"),
        ("Electronic Dig", "https://electronicdig.sites.oasis.unc.edu/")
    ]

    for name, link in chapter_names_links:
        chapters.append(tc.Chapter(name, link))

    chapter_paths = pathlib.Path(chapters_dir).glob("*.json")
    for chapter_path in chapter_paths:
        generate_chapter_modules(chapters, chapter_path)

    return chapters


def get_chapter_from_path(chapters, chapter_path):
    """
    Get the chapter element in a list corresponding to a path in /dig.
    Parameters
    ----------
    chapters : list of 'Chapter'
        Contains the Chapters that are searched for a match to the path
    chapter_path : str
        POSIX path to a chapter directory
    Returns
    -------
    chapter : Chapter
        The chapter in chapters corresponding to chapter_path
    """
    path_translator = {
        '/dig/html/part0': "Introduction",
        '/dig/html/part1': "Contents", # TODO Special case
        '/dig/html/part2': "Background",
        '/dig/html/part3': "Artifacts",
        '/dig/html/part4': "Food Remains",
        '/dig/html/part5': "Interpretations"
    }
    target = path_translator[chapter_path]
    for chapter in chapters:
        if chapter.name == target:
            return chapter


def generate_chapter_modules(chapters, chapter_path):
    """
    Process data for all modules of a chapter.
    Read the raw data from extraction phase for all of a chapter's modules, put
    that data into Module instances that are added as children of the passed
    Chapter instance.
    Parameters
    ----------
    chapters : list of 'Chapter'
        List of 'Chapter' objects, each decorated with all of the old site data
        for that chapter.
    chapter_path : Path
        Pathlib path to .json file containing the relevant chapter data.
    """

    # Load the extracted chapter data
    f = chapter_path.open()
    module_data = json.load(f)
    f.close()

    # Make sure we add modules to the right chapter
    chapter = get_chapter_from_path(chapters, module_data['path'])

    # Decorate the module-section-subsection subtree with data
    for module_entry in module_data['modules']:
        module = tc.Module(
            shortTitle=module_entry['module']['shortTitle'],
            fullTitle=module_entry['module']['fullTitle'],
            author=module_entry['module']['author']
        )
        for section in module_entry['module']['sections']:
            sec_href = (section['pageNum'] + section['name'] + ".html")
            this_section = tc.Section(
                name=section['name'],
                pageNum=section['pageNum'],
                href=sec_href.replace(' ', '_').replace('/', '_'),  # TODO temporary solution
                content=module_data['pages'][section['pageNum']]['content']
            )
            for subsection in section['subsections']:
                subsec_href = (subsection['pageNum'] + subsection['name'] + ".html")
                new_subsection = tc.Section(
                    name=subsection['name'],
                    pageNum=subsection['pageNum'],
                    href=subsec_href.replace(' ', '_').replace('/', '_'),  # TODO temporary solution
                    content=module_data['pages'][subsection['pageNum']]['content']
                )
                this_section.add_subsection(new_subsection)
            module.add_section(this_section)

        # Add the module subtree as child of the chapter
        chapter.add_module(module)

    return


def generate_text_pages(chapters):
    """
    Generate all text chapter pages.
    Parameters
    ----------
    chapters : list of 'Chapter'
        Data for all text chapters, represented by a list of decorated
        'Chapter' objects
    """

    # Jinja setup
    jinja_env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml']),
        line_statement_prefix='#',
        line_comment_prefix='##'
    )
    text_template = jinja_env.get_template('textpage.html.jinja')

    # Write the html files!
    for chapter in chapters:
        print(chapter.name)
        for module in chapter.modules:
            print(module.shortTitle)
            for section in module.sections:
                print(section.name)
                with open(section.href, 'x') as f:
                    f.write(text_template.render(
                        chapters=chapters,
                        this_chapter=chapter,
                        this_module=module,
                        this_section=section
                    ))
                for subsection in section.subsections:
                    with open(subsection.href, 'x') as f:
                        f.write(text_template.render(
                            chapters=chapters,
                            this_chapter=chapter,
                            this_module=module,
                            this_section=subsection
                        ))

    return


def generate_all_chapters(chapters_dir):
    """
    Generate pages for all text chapters from output of extraction phase.
    Main function of this file.
    Parameters
    ----------
    chapters_dir: str
        Path of the directory containing all text chapter data in POSIX Path
        format. Expects this directory to contain subdirectories for each named
        chapter. A text chapter subdirectory will contain JSON files for each
        module in that text chapter.
    """

    # Put the extracted data into a structure we can use for page generation
    chapters = generate_chapters(chapters_dir)

    # Set hrefs for chapters and modules such that the link leads to the first
    # page in that module/chapter
    for chapter in chapters:
        chapter.set_hrefs_r()
    # Make the files!
    generate_text_pages(chapters)
    return
