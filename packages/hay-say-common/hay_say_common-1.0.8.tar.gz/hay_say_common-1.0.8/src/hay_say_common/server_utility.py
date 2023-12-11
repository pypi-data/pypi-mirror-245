import json
import os
import subprocess
import traceback

from flask import request

"""Methods that are useful across multiple architecture servers"""


def clean_up(files_to_delete):
    if files_to_delete:
        for path in files_to_delete:
            os.remove(path)


def construct_full_error_message(architecture_root_dir, files_to_delete):
    message = construct_error_message(architecture_root_dir)
    try:
        clean_up(files_to_delete)
    except Exception:
        message += '\n\n...and failed to clean output directory, due to: \n' + traceback.format_exc(chain=False) + '\n'
    return message


def construct_error_message(architecture_root_dir):
    input_files = get_file_list(architecture_root_dir)
    return 'An error occurred while generating the output: \n' + traceback.format_exc() + \
           '\n\nPayload:\n' + json.dumps(request.json) + \
           '\n\nInput Audio Dir Listing: \n' + input_files


def get_file_list(folder):
    if os.path.exists(folder):
        return ', '.join(os.listdir(folder))
    else:
        return folder + ' does not exist'


def select_hardware(gpu_id):
    """Select which GPU will be used by setting the CUDA_VISIBLE_DEVICES environment variable. gpu_id can be an integer
    or a string. A typical values is '0', which will select the first CUDA-capable device. And empty string is also an
    acceptable value and will cause the CPU to be used instead of the GPU."""
    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
    return env

def get_gpu_info_from_another_venv(path_to_python_executable):
    """Returns a list of dictionaries containing the GPU ID, name, free memory, and total memory of each GPU that is
    visible to pytorch in the specified python environment. In Hay Say, there are often two virtual environments
    installed in a given container - one for the architecture and one for a Flask server that wraps the architecture in
    a REST interface. The Flask server does not have pytorch installed, but needs to know which GPUs are visible to the
    architecture, so this method is designed to remotely run commands on the other virtual environment, via the
    subprocess module. You can actually specify any python executable, but you'll probably want to specify the
    executable that is located in the architecture's virtual environment, e.g.
    "/root/hay_say/.venvs/so_vits_svc_4/bin/python3" """
    code = ['import torch; '
            'import json; '
            'gpu_info = [ '
            '    { '
            '        "Index": i, '
            '        "Name": torch.cuda.get_device_properties(i).name, '
            '        "Free Memory": torch.cuda.mem_get_info(i)[0], '
            '        "Total Memory": torch.cuda.mem_get_info(i)[1] '
            '    } '
            'for i in range(torch.cuda.device_count())]; '
            'print(json.dumps(gpu_info))']
    gpus = subprocess.check_output([path_to_python_executable, '-c', *code])
    return json.loads(gpus.decode('utf-8'))

