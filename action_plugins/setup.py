from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        def filter_dict(obj, filter):
            res = dict()
            for k, v in obj.items():
                if filter in k:
                    res[k] = v
                elif isinstance(v, dict):
                    val = filter_dict(v, filter)
                    if val is not None and val != dict():
                        res[k] = val
            return res

        result = super(ActionModule, self).run(tmp, task_vars)

        query = self._task.args.get('query', None)
        module_args = self._task.args.copy()
        if query:
            module_args.pop('query')

        module_return = self._execute_module(module_name='setup',
                                             module_args=module_args,
                                             task_vars=task_vars, tmp=tmp)

        if not module_return.get('failed') and query:
            return dict(ansible_facts=filter_dict(module_return['ansible_facts'], query))
        else:
            return module_return
