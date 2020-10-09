from modules import standard_text_chapters

if __name__ == "__main__":
    # Expects all .json files to be in chapters_directory
    # TODO Add ability to designate target directory
    chapters_directory = "/Users/"  # Your mileage may vary
    standard_text_chapters.generate_all_chapters(chapters_directory)
