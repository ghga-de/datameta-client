# Copyright 2021 Universität Tübingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pkg_resources import get_distribution

__version__ = get_distribution('datameta_client').version

# the major version of the API the server which the client is talking to
# should always match the version of the client, thus:
api_version = "v" + __version__.split(".")[0]
