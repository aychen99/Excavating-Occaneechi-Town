from modules import standard_text_chapters

if __name__ == "__main__":
    # Expects all .json files to be in chapters_directory
    # TODO add ability to designate target directory
    # TODO arg based execution
    chapters_directory = "/Users/"  # Change for your local machine
    standard_text_chapters.generate_all_chapters(chapters_directory)
