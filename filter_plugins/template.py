from jinja2 import Environment
import json

def template(item, tmplt, from_json=False):
    j2_env = Environment(block_start_string='<%',
                         block_end_string='%>',
                         variable_start_string='<<',
                         variable_end_string='>>')
    t = j2_env.from_string(tmplt)
    res = t.render(item=item)
    if from_json:
        return json.loads(res)
    else:
        return res

class FilterModule(object):

    def filters(self):
        return {
            'template': template
        }
