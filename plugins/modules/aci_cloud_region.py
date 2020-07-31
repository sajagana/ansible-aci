#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, nkatarmal-crest <nirav.katarmal@crestdatasys.com>
# Copyright: (c) 2020, Cindy Zhao <cizhao@cisco.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: aci_cloud_region
short_description: Manage Cloud Providers Region (cloud:Region)
description:
-  Manage Cloud Providers Region on Cisco Cloud ACI.
author:
- Nirav (@nirav)
- Cindy Zhao (@cizhao)
options:
  region:
    description:
    - The name of the cloud provider's region.
    aliases: [ name ]
    type: str
  cloud_provider_profile_vendor:
    description:
    - The vendor of the controller
    choices: [ aws ]
    type: str
    required: yes
  state:
    description:
    - Use C(present) or C(absent) for adding or removing.
    - Use C(query) for listing an object or multiple objects.
    choices: [ query ]
    default: query
    type: str
notes:
- More information about the internal APIC class B(cloud:Region) from
  L(the APIC Management Information Model reference,https://developer.cisco.com/docs/apic-mim-ref/).
- This module is used to query Cloud Providers Region.

extends_documentation_fragment:
- cisco.aci.aci
'''

EXAMPLES = r'''
- name: Query all regions
  cisco.aci.aci_cloud_region:
    host: apic
    username: userName
    password: somePassword
    validate_certs: no
    cloud_provider_profile_vendor: 'aws'
    state: query
  delegate_to: localhost

- name: Query a specific region
  cisco.aci.aci_cloud_region:
    host: apic
    username: userName
    password: somePassword
    validate_certs: no
    cloud_provider_profile_vendor: 'aws'
    region: eu-west-2
    state: query
  delegate_to: localhost
'''

RETURN = r'''
current:
  description: The existing configuration from the APIC after the module has finished
  returned: success
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production environment",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
error:
  description: The error information as returned from the APIC
  returned: failure
  type: dict
  sample:
    {
        "code": "122",
        "text": "unknown managed object class foo"
    }
raw:
  description: The raw output returned by the APIC REST API (xml or json)
  returned: parse error
  type: str
  sample: '<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1"><error code="122" text="unknown managed object class foo"/></imdata>'
sent:
  description: The actual/minimal configuration pushed to the APIC
  returned: info
  type: list
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment"
            }
        }
    }
previous:
  description: The original configuration from the APIC before the module has started
  returned: info
  type: list
  sample:
    [
        {
            "fvTenant": {
                "attributes": {
                    "descr": "Production",
                    "dn": "uni/tn-production",
                    "name": "production",
                    "nameAlias": "",
                    "ownerKey": "",
                    "ownerTag": ""
                }
            }
        }
    ]
proposed:
  description: The assembled configuration from the user-provided parameters
  returned: info
  type: dict
  sample:
    {
        "fvTenant": {
            "attributes": {
                "descr": "Production environment",
                "name": "production"
            }
        }
    }
filter_string:
  description: The filter string used for the request
  returned: failure or debug
  type: str
  sample: ?rsp-prop-include=config-only
method:
  description: The HTTP method used for the request to the APIC
  returned: failure or debug
  type: str
  sample: POST
response:
  description: The HTTP response from the APIC
  returned: failure or debug
  type: str
  sample: OK (30 bytes)
status:
  description: The HTTP status from the APIC
  returned: failure or debug
  type: int
  sample: 200
url:
  description: The HTTP url used for the request to the APIC
  returned: failure or debug
  type: str
  sample: https://10.11.12.13/api/mo/uni/tn-production.json
'''

from ansible_collections.cisco.aci.plugins.module_utils.aci import ACIModule, aci_argument_spec
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = aci_argument_spec()
    argument_spec.update(
        region=dict(type='str', aliases=["name"]),
        cloud_provider_profile_vendor=dict(type='str', choices=['aws'], required=True),
        state=dict(type='str', default='query', choices=['query']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    region = module.params.get('region')
    cloud_provider_profile_vendor = module.params.get('cloud_provider_profile_vendor')
    state = module.params.get('state')

    aci = ACIModule(module)
    aci.construct_url(
        root_class=dict(
            aci_class='cloudProvP',
            aci_rn='clouddomp/provp-{0}'.format(cloud_provider_profile_vendor),
            target_filter='eq(cloudProvP.vendor, "{0}")'.format(cloud_provider_profile_vendor),
            module_object=cloud_provider_profile_vendor
        ),
        subclass_1=dict(
            aci_class='cloudRegion',
            aci_rn='region-{0}'.format(region),
            target_filter='eq(cloudRegion.name, "{0}")'.format(region),
            module_object=region
        ),
        child_classes=[]
    )

    aci.get_existing()

    aci.exit_json()


if __name__ == "__main__":
    main()