import platform
import psutil
import pandas as pd
from datetime import datetime
from IPython.display import display, HTML
import GPUtil
import importlib

def pkg_system_info(packages, show_pkg=True, show_gpu=True, show_system=True):
    """
    This function takes a list of package names as input, imports each package dynamically, 
    and displays the version information of each package and the system information.

    Parameters:
    packages (list of str): A list of package names to import and get version information.
    show_pkg (bool): Whether to show package version information. Default is True.
    show_system (bool): Whether to show system information. Default is True.
    show_gpu (bool): Whether to show GPU information. Default is True.

    Returns:
    None

    Example:
    >>> pkg_system_info(['numpy', 'pandas', 'scipy', 'qiskit'], show_pkg=True, show_gpu=True, show_system=False)
    """

    if show_pkg:
        # Get packages version information
        pkg_versions = []
        for pkg_name in packages:
            try:
                pkg = importlib.import_module(pkg_name)
                version = pkg.__version__
            except AttributeError:
                version = "Version not available"
            pkg_versions.append((pkg.__name__, version))
        
        pkg_versions_df = pd.DataFrame(pkg_versions, columns=['Package', 'Version'])
        display(HTML(pkg_versions_df.to_html(index=False)))

    if show_gpu:
        # Get GPU information
        gpus = GPUtil.getGPUs()
        gpu_info = {'GPU Version': gpus[0].name, 'GPU Memory': f"{round(gpus[0].memoryTotal / 1024, 1)} Gb"} if gpus else {'GPU Version': 'No GPU detected', 'GPU Memory': 'N/A'}
        gpu_info_df = pd.DataFrame(list(gpu_info.items()), columns=['GPU Information', 'Details'])
        display(HTML(gpu_info_df.to_html(index=False)))

    if show_system:
        # Get system information
        system_info = {
            'Python version': platform.python_version(),
            'Python compiler': platform.python_compiler(),
            'Python build': platform.python_build(),
            'OS': platform.system(),
            'CPU Version': platform.processor(),
            'CPU Number': psutil.cpu_count(),
            'CPU Memory': f"{round(psutil.virtual_memory().total / (1024.0 **3), 1)} Gb",
            'Time': datetime.now().strftime("%a %b %d %H:%M:%S %Y %Z")
        }
        system_info_df = pd.DataFrame(list(system_info.items()), columns=['System Information', 'Details'])
        display(HTML(system_info_df.to_html(index=False)))