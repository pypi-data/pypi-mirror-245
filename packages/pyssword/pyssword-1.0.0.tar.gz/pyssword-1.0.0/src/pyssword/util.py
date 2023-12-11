import inspect
import subprocess


def doc(arg):
    """Docstring decorator.

    arg:    Docstring text or object.
    """
    def decorator(func):
        if type(arg) is str:
            func.__doc__ = arg
        elif inspect.isclass(arg):
            func.__doc__ = arg.__doc__
        else:
            func.__doc__ = None

        return func
    return decorator


def send_to_clipboard(data, duration):
    """Sends data to the clipboard asynchronously and clears it after
    the duration time.
    """

    command = f"""
        # Copy data to clipboard
        echo -n "{data}" | xclip -in -rmlastnl -selection clipboard

        # Wait for the specified duration
        sleep {duration}

        # Clear clipboard after the duration
        xclip -selection clipboard -t text /dev/null
    """

    subprocess.Popen(command, shell=True, executable='/bin/bash')


def get_from_clipboard(timeout=3):
    """Gets data from the clipboard asynchronously.
    """

    command = f"""
        # Copy data from clipboard
        xclip -out -rmlastnl -selection clipboard ; echo
    """

    proc = subprocess.Popen(
        command,
        shell=True,
        executable='/bin/bash',
        stdout=subprocess.PIPE,
        text=True
    )

    try:
        output, error = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        output, error = proc.communicate()

    return output
