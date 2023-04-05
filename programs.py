def identify_firefox(user_processes):
    for p in user_processes:
        if "/usr/lib64/firefox/firefox" in p:
            return "firefox"
