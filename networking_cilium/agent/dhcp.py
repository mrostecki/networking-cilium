# Copyright (c) 2019 SUSE LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron.agent.dhcp import agent as dhcp_agent


class Watcher(object):
    def on_endpoint_set(self, response, name):
        pass

class CiliumDhcpAgent(dhcp_agent.DhcpAgent):
    def __init__(self):
        hostname = socket.gethostname()
        super(CiliumDhcpAgent, self).__init__(host=hostname)
