from ansible.plugins.callback import CallbackBase
from subprocess import call
from platform import system as get_system_name

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'notify_me'
    CALLBACK_NEEDS_WHITELIST = True

    def v2_playbook_on_stats(self, stats):

        def notify(msg,is_error=False):
            sys_name = get_system_name()
            if sys_name == 'Darwin':
                sound = "Basso" if is_error else "default"
                call(["osascript", "-e",
                    'display notification "{}" with title "Ansible" sound name "{}"'.
                    format(msg,sound)])
            elif sys_name == 'Linux':
                icon = "dialog-warning" if is_error else "dialog-info"
                rc = call(["notify-send", "-i", icon, "Ansible", msg])
                print "error code {}".format(rc)

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
