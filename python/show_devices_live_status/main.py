# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.dp import Action
import requests


# ---------------
# ACTIONS EXAMPLE
# ---------------
class showAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        self.log.info('action input.command: ', input.command)
        with ncs.maapi.single_read_trans('admin', 'python') as t:
            root = ncs.maagic.get_root(t)
            devs = root.devices.device
            for dev in devs:
                show = devs[dev.name].live_status.__getitem__('exec').show
                inp = show.get_input()
                inp.args = [input.command]
                res = show.request(inp)
                self.log.info('Show: {}'.format(res.result))
                output.result = res.result

        # Updating the output data structure will result in a response
        # being returned to the caller.
# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.

        # When using actions, this is how we register them:
        #
        self.register_action('show-devices-live-status-action', showAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
