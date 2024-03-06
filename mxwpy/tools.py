import platform
import psutil
import pandas as pd
from datetime import datetime
from IPython.display import display, HTML
import GPUtil
import importlib
import subprocess

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

    def get_cpu_info():
        # Get CPU information on Linux
        cpu_info = subprocess.check_output("lscpu", shell=True).decode()
        architecture = subprocess.check_output("uname -m", shell=True).decode().strip()
        lines = cpu_info.split('\n')
        info_dict = {}
        for line in lines:
            if "Vendor ID:" in line:
                info_dict['Vendor ID'] = line.split(':')[1].strip()
            if "CPU family:" in line:
                info_dict['CPU family'] = line.split(':')[1].strip()
            if "Model:" in line:
                info_dict['Model'] = line.split(':')[1].strip()
            if "Stepping:" in line:
                info_dict['Stepping'] = line.split(':')[1].strip()
        return architecture, info_dict


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

        if system_info['OS'] == 'Linux':
            architecture, cpu_info = get_cpu_info()
            system_info['CPU Version'] = f"{architecture} Family {cpu_info['CPU family']} Model {cpu_info['Model']} Stepping {cpu_info['Stepping']}, {cpu_info['Vendor ID']}"

        system_info_df = pd.DataFrame(list(system_info.items()), columns=['System Information', 'Details'])
        display(HTML(system_info_df.to_html(index=False)))