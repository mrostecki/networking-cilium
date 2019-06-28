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

from neutron.agent.linux import utils as agent_utils

from networking_cilium.ciliumclient import client


class CiliumAgent(object):
    def __init__(self):
        self.client = client.CiliumClient()

    def start(self):
        server = agent_utils.UnixDomainWSGIServer('networking-cilium-agent')
        server.start()

    def sync(self):
        ensure_all_networks_provisioned()

    def ensure_all_networks_provisioned(self):
        ports = []
        datapaths = {str(p.datapath.uuid) for p in ports if p.type == ''}
        namespaces = []
        # Make sure that all those datapaths are serving metadata
        for datapath in datapaths:
            netns = self.provision_datapath(datapath)
            if netns:
                namespaces.append(netns)

        return namespaces

    @staticmethod
    def _get_veth_name(datapath):
        return ['{}{}{}'.format(n_const.TAP_DEVICE_PREFIX,
                                datapath[:10], i) for i in [0, 1]]

    def teardown_datapath(self, datapath):
        veth_name = self._get_veth_name(datapath)
        self.ovs_idl.del_port(veth_name[0]).execute()
        if ip_lib.device_exists(veth_name[0]):
            ip_lib.IPWrapper().del_veth(veth_name[0])

    def update_datapath(self, datapath):
        self.provision_datapath(datapath)
        self.teardown_datapath(datapath)

    def provision_datapath(self, datapath):
        ip1 = ip_lib.IPDevice(veth_name[0])
        if ip_lib.device_exists(veth_name[1], namespace):
            ip2 = ip_lib.IPDevice(veth_name[1], namespace)
        else:
            LOG.debug("Creating VETH %s in %s namespace", veth_name[1],
                      namespace)
            # Might happen that the end in the root namespace exists even
            # though the other end doesn't. Make sure we delete it first if
            # that's the case.
            if ip1.exists():
                ip1.link.delete()
            ip1, ip2 = ip_lib.IPWrapper().add_veth(
                veth_name[0], veth_name[1], namespace)

        # Make sure both ends of the VETH are up
        ip1.link.set_up()
        ip2.link.set_up()

        # Configure the MAC address.
        ip2.link.set_address(metadata_port.mac)
        dev_info = ip2.addr.list()

        self.client.create_endpoint('123')


def main():
    agt = CiliumAgent()
    agt.start()
