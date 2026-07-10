def prompt_yesno(question):
    """Prompt the user with a yes/no question."""
    while True:
        ans = input(f"{question} [y/n]: ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
