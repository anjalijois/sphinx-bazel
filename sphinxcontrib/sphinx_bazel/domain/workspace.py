"""
bazel-workspace
===============
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.locale import _


class BazelWorkspace(Directive):
    """
    Directive to mark description of a new workspace.
    """
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'path':  directives.unchanged
    }
    
    def run(self):
        env = self.state.document.settings.env
        workspace_name = self.arguments[0].strip()
        workspace_path = self.options.get('path', '')
        env.ref_context['bazel:workspace'] = workspace_name
        ret = []
        
        env.domaindata['bazel']['workspaces'][workspace_name] = (env.docname,
                                                                 workspace_path)
        # make a duplicate entry in 'objects' to facilitate searching for
        # the module in PythonDomain.find_obj()
        env.domaindata['bazel']['objects'][workspace_name] = (env.docname, 'workspace')
        targetnode = nodes.target('', '', ids=['workspace-' + workspace_name],
                                  ismod=True)
        self.state.document.note_explicit_target(targetnode)
        # the platform and synopsis aren't printed; in fact, they are only
        # used in the modindex currently
        ret.append(targetnode)
        indextext = _('%s (workspace)') % workspace_name
        inode = addnodes.index(entries=[('single', indextext,
                                         'module-' + workspace_name, '', None)])
        ret.append(inode)
        return ret
