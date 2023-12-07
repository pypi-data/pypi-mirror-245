#  Drakkar-Software trading-backend
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import trading_backend.exchanges as exchanges


class GateIO(exchanges.Exchange):
    SPOT_ID = "Octobot"
    MARGIN_ID = "Octobot"
    FUTURE_ID = "Octobot"
    IS_SPONSORING = True
    HEADER_KEY = "X-Gate-Channel-Id"

    @classmethod
    def get_name(cls):
        return 'gateio'

    def get_headers(self):
        return {self.HEADER_KEY: self._get_id()}
