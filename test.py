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

print(f"Shared Secret: {shared_secret}")
print(f"Identity Secret: {identity_secret}")
print(f"Device ID: {device_id}")
print(f"Device ID2: {device_id2}")
print(f"Auth Code: {auth_code}")

cookies = stcookie.getCookies('https://steamcommunity.com')
trades = steam_auth.get_trades(identity_secret, cookies)

print(f"\nCurrent trades: {trades}\n")

for index in range(len(trades['trade_id'])):
    print(
        f"I\'ll accept {trades['trade_id'][index]} with the key {trades['trade_key'][index]}"
    )

    response = steam_auth.finalize_trade(cookies, identity_secret, trades['trade_id'][index], trades['trade_key'][index], 'accept')

    print(
        f"trade accepted! ({response.content.decode(locale.getpreferredencoding())})"
    )
