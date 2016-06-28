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

import base64
import codecs
import hashlib
import hmac
import sys

import requests

STEAM_ALPHABET = ['2', '3', '4', '5', '6', '7', '8', '9',
                  'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K',
                  'M', 'N', 'P', 'Q', 'R', 'T', 'V', 'W',
                  'X', 'Y']


def get_authentication_code(secret):
    query_time_url = 'https://api.steampowered.com/ITwoFactorService/QueryTime/v1'
    response = requests.post(query_time_url, headers={'user-agent':'Unknown/0.0.0'})
    server_time = int(response.json()['response']['server_time'])
    offset = server_time + response.elapsed.seconds
    msg = int(offset / 30).to_bytes(8, 'big')
    key = base64.b64decode(secret)
    auth = hmac.new(key, msg, hashlib.sha1)
    digest = auth.digest()
    start = digest[19] & 0xF
    code = digest[start:start + 4]
    auth_code_raw = int(codecs.encode(code, 'hex'), 16) & sys.maxsize

    auth_code = []
    for i in range(5):
        auth_code.append(STEAM_ALPHABET[int(auth_code_raw % len(STEAM_ALPHABET))])
        auth_code_raw /= len(STEAM_ALPHABET)

    return ''.join(auth_code)

def get_device_id(username):
    hex_digest = hashlib.sha1(username.encode()).hexdigest()
    device_id = [ 'android:' ]

    for (start, end) in ([0, 8],[9, 13],[14, 18],[19, 23],[24, 32]):
        device_id.append(hex_digest[start:end])
        device_id.append('-')

    device_id.pop(-1)
    return ''.join(device_id)
