from ansible.plugins.callback import CallbackBase
from subprocess import call

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'osx_notify'
    CALLBACK_NEEDS_WHITELIST = True

    def v2_playbook_on_stats(self, stats):

        def notify(msg,is_error=False):
            sound = "Basso" if is_error else "default"
            call(["osascript", "-e",
              'display notification "{}" with title "Ansible" sound name "{}"'.
              format(msg,sound)])

        hosts = stats.processed.keys()
        failed_hosts = []

        for h in hosts:
            t = stats.summarize(h)
            if t['unreachable'] + t['failures'] > 0:
                failed_hosts.append(h)

        if len(failed_hosts) > 0:
            notify("Failed hosts: {}".format(" ".join(failed_hosts)),True)
        else:
            notify("Job's done!")
