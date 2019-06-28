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

from neutron_lib.api.definitions import portbindings

from networking_cilium.ciliumclient import client


class CiliumMechanismDriver(mech_agent.SimpleAgentMechanismDriverBase):
    def __init__(self):
        self.client = client.CiliumClient()
        vif_details = {
            'port_filter': True,
            'mac_address': ''
        }
        super(CiliumMechanismDriver, self).__init__(
            'CILIUM',
            portbindings.VIF_TYPE_BRIDGE,
            vif_details)

    def get_allowed_network_types(self, agent=None):
        return ('local', 'flat')

    def get_mappings(self, agent):
        assert False

    def create_port_precommit(self, context):
        super(CiliumMechanismDriver, self).create_port_precommit(context)

    def create_port_postcommit(self, context):
        for fixed_ip in context._port['fixed_ips']:
            self.client.allocate_ip(fixed_ip)
        super(CiliumMechanismDriver, self).create_port_postcommit(context)

    def update_port_precommit(self, context):
        super(CiliumMechanismDriver, self).update_port_precommit(context)

    def update_port_postcommit(self, context):
        super(CiliumMechanismDriver, self).update_port_postcommit(context)

    def delete_port_precommit(self, context):
        super(CiliumMechanismDriver, self).delete_port_precommit(context)

    def delete_port_postcommit(self, context):
        super(CiliumMechanismDriver, self).delete_port_postcommit(context)
