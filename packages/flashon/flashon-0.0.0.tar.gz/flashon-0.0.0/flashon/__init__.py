from setuptools import setup
from functools import wraps

def flash_event(func):
    @wraps(func)
    def wrapper(name,version,author,requires):
        setup(
            name=name,version=version,author=author,install_requires=requires,
            zip_safe=False
            )
        return
    return wrapper
    
