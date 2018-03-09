#!/usr/bin/env python3
#
#  Copyright (C) 2016 Codethink Limited
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. If not, see <http://www.gnu.org/licenses/>.
#
#  Authors:
#        Tristan Van Berkom <tristan.vanberkom@codethink.co.uk>
#        Jürg Billeter <juerg.billeter@codethink.co.uk>

# System imports
import os

# BuildStream toplevel imports
from ..plugin import _plugin_lookup
from .. import SourceError
from .. import _yaml

# Local imports
from . import Queue, QueueStatus, QueueType


# A queue which tracks sources
#
class TrackQueue(Queue):

    action_name = "Track"
    complete_name = "Tracked"
    queue_type = QueueType.FETCH

    def process(self, element):
        return element._track()

    def status(self, element):
        # We can skip elements entirely if they have no sources.
        if not list(element.sources()):
            return QueueStatus.SKIP

        return QueueStatus.READY

    def done(self, element, result, returncode):

        if returncode != 0:
            return False

        changed = False

        # Set the new refs in the main process one by one as they complete
        for unique_id, new_ref in result:
            source = _plugin_lookup(unique_id)
            try:
                source._save_ref(new_ref)
            except SourceError as e:
                # FIXME: We currently dont have a clear path to
                #        fail the scheduler from the main process, so
                #        this will just warn and BuildStream will exit
                #        with a success code.
                #
                source.warn("Failed to update project file",
                            detail="{}".format(e))

        context = element._get_context()
        context._push_message_depth(True)
        element._update_state()
        context._pop_message_depth()

        # We'll appear as a skipped element if tracking resulted in no change
        return changed
