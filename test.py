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

import locale

from stlib import stcookie, stconfig
stconfig.getParser()

import importlib
steam_auth = importlib.__import__('steam-auth')

shared_secret = steam_auth.get_key('shared_secret')
identity_secret = steam_auth.get_key('identity_secret')
device_id = steam_auth.get_device_id()
device_id2 = steam_auth.generate_device_id('SteamUserName')
auth_code = steam_auth.get_authentication_code(shared_secret)

print("Shared Secret: {}".format(shared_secret))
print("Identity Secret: {}".format(identity_secret))
print("Device ID: {}".format(device_id))
print("Device ID2: {}".format(device_id2))
print("Auth Code: {}".format(auth_code))

cookies = stcookie.getCookies('https://steamcommunity.com')
trades = steam_auth.get_trades(identity_secret, cookies)

print("\nCurrent trades: {}\n".format(trades))

for index in range(len(trades['trade_id'])):
    print('I\'ll accept {} with the key {}'.format(trades['trade_id'][index], trades['trade_key'][index]))

    response = steam_auth.finalize_trade(cookies, identity_secret, trades['trade_id'][index], trades['trade_key'][index], 'accept')

    print("trade accepted! ({})".format(response.content.decode(locale.getpreferredencoding())))
