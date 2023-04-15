from pathlib import Path
import subprocess
import atexit
import signal
from django.core.signals import request_started, request_finished
from django.dispatch import receiver


# Define a function to start the JAR file
@receiver(request_started)
def start_jar(sender, **kwargs):
    global process
    dir=Path(__file__).resolve().parent
    process = subprocess.Popen(['java', '-jar', str(dir)+'\\emailapi.jar'])

# Define a function to stop the JAR file
@receiver(request_finished)
def stop_jar(sender, **kwargs):
    global process
    process.terminate()
