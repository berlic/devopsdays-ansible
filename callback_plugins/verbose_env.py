from ansible.plugins.callback import CallbackBase
import os

try:
    from __main__ import display
except ImportError:
    display = None

class CallbackModule(CallbackBase):

    def v2_playbook_on_start(self, playbook):
        v = os.environ.get('ANSIBLE_VERBOSITY')
        if v and display:
            display.display(
                'Verbosity is set to {} with environment variable.'.format(v),
                color='blue')
            display.verbosity = int(v)
