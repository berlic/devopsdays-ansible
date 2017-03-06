#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: osx_volume
short_description: Set OS X volume level
options:
    level:
        description:
            - Volume level to be applied
        aliases:
            - volume
        required: false
    muted:
        description:
            - Set mute on/off
        required: false

author:
    - Konstantin Suvorov
'''

EXAMPLES = '''

- name: Set volume to 25
  osx_volume:
    level: 25

- name: Mute
  osx_volume:
    muted: yes

'''

from ansible.module_utils.basic import AnsibleModule
from subprocess import call, check_output

def get_volume():
    level = check_output(['osascript','-e','output volume of (get volume settings)']).strip()
    muted = check_output(['osascript','-e','output muted of (get volume settings)']).strip()
    muted = (muted.lower() == "true")
    return (int(level), muted)

def set_volume(level=None, muted=None):
    if level is not None:
        call(['osascript','-e','set volume output volume {}'.format(level)])
    if muted is not None:
        mute_str = 'true' if muted else 'false'
        call(['osascript','-e','set volume output muted {}'.format(mute_str)])
    return get_volume()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            level=dict(type='int', required=False, default=None, aliases=['volume']),
            muted=dict(type='bool', required=False, default=None)
        ),
        supports_check_mode=True
    )
    req_level = module.params['level']
    req_muted = module.params['muted']

    l, m = get_volume()
    result = dict(level=(req_level if req_level is not None else l),
                  muted=(req_muted if req_muted is not None else m),
                  changed=False)

    if req_level is not None and l != req_level:
        result['changed'] = True
    elif req_muted is not None and m != req_muted:
        result['changed'] = True

    if module.check_mode or not result['changed']:
        module.exit_json(**result)

    new_l, new_m = set_volume(level=req_level, muted=req_muted)

    if req_level is not None and new_l != req_level:
        module.fail_json(msg="Failed to set requested volume level {} (actual {})!".format(req_level, new_l))
    if req_muted is not None and new_m != req_muted:
        module.fail_json(msg="Failed to set requested mute flag {} (actual {})!".format(req_muted, new_m))

    module.exit_json(**result)

if __name__ == '__main__':
    main()
