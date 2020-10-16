from jinja2 import Environment, FileSystemLoader, select_autoescape
from os.path import relpath
import json
import pathlib
from ..site_data_structs import text
from .. import utilities


def process_chapters(chapter_paths, out_dir, tables):
    """
    Define the structure of the site's text chapters for sidebar.
    Populates a list, 'chapters', with the basic chapter structure information
    required to generate page sidebars.
    Parameters
    ----------
    chapters_dir : Path
        Path to the directory with the chapter data files.
    Returns
    -------
    chapters : List of 'Chapter' objects
        List of 'Chapter' objects, each populated with all of the old site data
        for that chapter.
    """

    print("Processing text chapter data.")

    chapters = []

    # TODO: reconsider chapter structure hardcoding
    chapter_names = [
        "Getting Started",
        "Archaeology Primer",
        "Introduction",
        "Contents",
        "Background",
        "Excavations",
        "Artifacts",
        "Food Remains",
        "Interpretations",
        "Electronic Dig"
    ]

    # Create all chapter objects
    for name in chapter_names:
        if name == "Electronic Dig":
            ch = text.Chapter(name, None)
            ch.set_href(pathlib.Path("https://electronicdig.sites.oasis.unc.edu/"))
            chapters.append(ch)
        else:
            chapter_path = out_dir / name.lower().replace(' ', '')
            chapters.append(text.Chapter(name, chapter_path))

    # Process data per chapter
    for chapter_path in chapter_paths:
        process_chapter(chapters, chapter_path, tables)

    print("Finished processing text chapter data.")

    return chapters


def get_chapter_from_path(chapters, chapter_path):
    """
    Get the chapter element in a list corresponding to a path in /dig.
    Parameters
    ----------
    chapters : list of 'Chapter'
        Contains the Chapters that are searched for a match to the path
    chapter_path : Path
        Path to a chapter directory
    Returns
    -------
    chapter : Chapter
        The chapter in chapters corresponding to chapter_path
    """

    path_translator = {
        '/dig/html/part0': "Introduction",
        '/dig/html/part1': "Contents",
        '/dig/html/part2': "Background",
        '/dig/html/part3': "Artifacts",
        '/dig/html/part4': "Food Remains",
        '/dig/html/part5': "Interpretations"
    }
    target = path_translator[str(chapter_path)]
    for chapter in chapters:
        if chapter.name == target:
            return chapter

    return None


def generate_section_filename(page_num, page_name):
    """
    Creates a output Path for a section file.
    Format is 'XXX_page_name.html', or 'prelimsXX_page_name.html' for front
    matter pages.
    Parameters
    ----------
    page_num : str
    page_name : str
    Returns
    -------
    Path
    """

    page_name = utilities.str_ops.make_str_filename_safe(page_name)

    path_str = '{}_{}.html'.format(utilities.str_ops.normalize_file_page_num(page_num),
                                   page_name)
    return pathlib.Path(path_str)


def process_chapter(chapters, chapter_path, tables):
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
    with chapter_path.open() as f:
        module_data = json.load(f)

    # Make sure we add modules to the right chapter
    chapter = get_chapter_from_path(chapters, module_data['path'])

    # Decorate the module-section-subsection subtree with data
    for module_entry in module_data['modules']:
        module = text.Module(
            short_title=module_entry['module']['shortTitle'],
            full_title=module_entry['module']['fullTitle'],
            author=module_entry['module']['author']
        )
        for section in module_entry['module']['sections']:
            sec_href = chapter.path / generate_section_filename(
                section['pageNum'], section['name'])

            this_section = text.Section(
                name=section['name'],
                page_num=section['pageNum'],
                href=sec_href,
                content=module_data['pages'][section['pageNum']]['content']
            )

            # Add to path table for link resolution
            tables.path_table.register(
                section['path'], this_section.href, this_section)

            # Add to page table for pagination
            tables.page_table.register(
                this_section.page_num, this_section.href)

            for subsection in section['subsections']:
                subsec_href = chapter.path / generate_section_filename(
                    subsection['pageNum'], subsection['name'])

                this_subsection = text.Section(
                    name=subsection['name'],
                    page_num=subsection['pageNum'],
                    href=subsec_href,
                    content=module_data['pages'][subsection['pageNum']]['content']
                )

                # Add to path table for link resolution
                tables.path_table.register(
                    subsection['path'], this_subsection.href, this_subsection)

                # Add to page table for pagination
                tables.page_table.register(
                    this_subsection.page_num, this_subsection.href)

                this_section.add_subsection(this_subsection)

            module.add_section(this_section)

            # Add to path table for link resolution
            tables.path_table.register(module_entry['module']['path'], module.href, module)

        # Add the module subtree as child of the chapter
        chapter.add_module(module)

        # Add to path table for link resolution
        tables.path_table.register(module_data['path'], chapter.href, chapter)

    return


def write_text_pages(chapters, tables):
    """
    Generate all text chapter pages.
    Parameters
    ----------
    chapters : list of 'Chapter'
        Data for all text chapters, represented by a list of decorated
        'Chapter' objects
    """

    print("Writing text chapter pages.")

    # Jinja setup
    templates_path = str((pathlib.Path(__file__).parent.parent / "templates"))
    jinja_env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html', 'xml']),
        line_statement_prefix='#',
        line_comment_prefix='##',
        trim_blocks=True
    )
    text_template = jinja_env.get_template('textpage.html.jinja')

    # Write the html files!
    for chapter in chapters:
        # Should have better solution here, restructure method
        if chapter.name != "Excavations":
            for module in chapter.modules:
                chapters_rel = [
                    c.get_dict_with_relpaths(module.href) for c in chapters]
                for section in module.sections:
                    # Next block should have its own function
                    prev_href = tables.page_table.get_prev_page_href(section.page_num)
                    if prev_href is not None:
                        prev_href_rel = utilities.path_ops.rel_path(prev_href, section.href)
                    else:
                        prev_href_rel = None
                    next_href = tables.page_table.get_next_page_href(section.page_num)
                    if next_href is not None:
                        next_href_rel = utilities.path_ops.rel_path(next_href, section.href)
                    else:
                        next_href_rel = None

                    pagination = {
                        'prev_page_href': prev_href_rel,
                        'this_page_num': section.page_num,
                        'next_page_href': next_href_rel
                    }

                    section.href.parent.mkdir(parents=True, exist_ok=True)
                    with section.href.open('w') as f:
                        f.write(text_template.render(
                            chapters=chapters_rel,
                            this_chapter_name=chapter.name,
                            this_module_name=module.full_title,
                            this_section_name=section.name,
                            this_section=section.get_dict_with_relpaths(section.href),
                            pagination=pagination
                        ))
                    for subsection in section.subsections:
                        # Next block should have its own function
                        prev_href = tables.page_table.get_prev_page_href(subsection.page_num)
                        if prev_href is not None:
                            prev_href_rel = utilities.path_ops.rel_path(prev_href, subsection.href)
                        else:
                            prev_href_rel = None
                        next_href = tables.page_table.get_next_page_href(subsection.page_num)
                        if next_href is not None:
                            next_href_rel = utilities.path_ops.rel_path(next_href, subsection.href)
                        else:
                            next_href_rel = None

                        pagination = {
                            'prev_page_href': prev_href_rel,
                            'this_page_num': subsection.page_num,
                            'next_page_href': next_href_rel
                        }
                        subsection.href.parent.mkdir(parents=True, exist_ok=True)
                        with subsection.href.open('w') as f:
                            f.write(text_template.render(
                                chapters=chapters_rel,
                                this_chapter_name=chapter.name,
                                this_module_name=module.full_title,
                                this_section_name=subsection.name,
                                this_section=subsection.get_dict_with_relpaths(subsection.href),
                                pagination=pagination
                            ))

    print("Finished writing text chapter pages.")

    return
