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

import requests_unixsocket


FORMAT_STR = "http+unix://{}/{}"
SOCK_PATH = "%2Fvar%2Frun%2Fcilium%2Fcilium.sock"


class CiliumClient(object):
    def __init__(self):
        self.session = requests_unixsocket.Session()

    def _get(self, path, *args, **kwargs):
        return self.session.get(FORMAT_STR.format(SOCK_PATH, path),
                                *args, **kwargs)

    def _post(self, path, *args, **kwargs):
        return self.session.post(FORMAT_STR.format(SOCK_PATH, path),
                                 *args, **kwargs)

    def _put(self, path, *args, **kwargs):
        return self.session.put(FORMAT_STR.format(SOCK_PATH, path),
                                *args, **kwargs)

    def allocate_ip(self, addr):
        return self._post('ipam/{}'.format(addr))

    def create_endpoint(self, endpoint_id):
        return self._put('endpoint/{}'.format(endpoint_id))
