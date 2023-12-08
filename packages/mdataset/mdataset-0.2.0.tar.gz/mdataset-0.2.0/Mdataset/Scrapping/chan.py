def chan4scrap(board_name, num_threads=10, debug=False):
    try:
        from scap4chan import scrape4chan_board
    except ImportError:
        print("scap4chan module not found. Installing...")
        try:
            import subprocess
            subprocess.check_call(['pip', 'install', 'scap4chan'])
            from scap4chan import scrape4chan_board
        except Exception as install_error:
            print(f"Failed to install scap4chan: {install_error}")
            return

    try:
        scrape4chan_board(board_name, num_threads=num_threads, debug=debug)
        print(f"Scraping for /{board_name}/ completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
