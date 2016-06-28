#!/usr/bin/env python
#
# Lara Maia <dev@lara.click> 2016
#
# The Steam Tools is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# The Steam Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#

import importlib
import json
import locale
import subprocess

steam_auth = importlib.__import__('steam-auth')


def get_data_json(adb_path, steam_path):
    data = subprocess.check_output([adb_path,
                                    'shell',
                                    'su',
                                    '-c',
                                    'cat ' + steam_path + '/files/Steamguard-*'])

    return json.loads(data.decode(locale.getpreferredencoding()))


data = get_data_json('/usr/bin/adb', '/data/data/com.valvesoftware.android.steam.community')
shared_secret = data['shared_secret']
identity_secret = data['identity_secret']
device_id = steam_auth.get_device_id('SteamUserName')
auth_code = steam_auth.get_authentication_code(shared_secret)

print("Shared Secret: {}".format(shared_secret))
print("Identity Secret: {}".format(identity_secret))
print("Device ID: {}".format(device_id))
print("Auth Code: {}".format(auth_code))
