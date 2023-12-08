#
#  Copyright (c) 2015 - 2023, Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause
#

"""Json schemas used by geopmdpy

GEOPM_ACTIVE_SESSIONS_SCHEMA:

.. code-block:: json

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "https://geopm.github.io/active_sessions.schema.json",
        "title": "ActiveSession",
        "type": "object",
        "properties": {
          "client_pid": {
            "type": "integer"
          },
          "client_uid": {
            "type": "integer",
            "minimum": 0
          },
          "client_gid": {
            "type": "integer",
            "minimum": 0
          },
          "create_time": {
            "type": "number",
            "minimum": 0
	  },
          "reference_count": {
            "type": "integer",
            "minimum": 0
          },
          "signals": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "controls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "watch_id": {
            "type": "integer"
          },
          "batch_server": {
            "type": "integer"
          },
          "profile_name": {
            "type": "string"
          }
        },
        "required": ["client_pid", "client_uid", "client_gid", "create_time", "signals", "controls"],
        "additionalProperties": false
    }


"""

GEOPM_ACTIVE_SESSIONS_SCHEMA = """
    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "https://geopm.github.io/active_sessions.schema.json",
        "title": "ActiveSession",
        "type": "object",
        "properties": {
          "client_pid": {
            "type": "integer"
          },
          "client_uid": {
            "type": "integer",
            "minimum": 0
          },
          "client_gid": {
            "type": "integer",
            "minimum": 0
          },
          "create_time": {
            "type": "number",
            "minimum": 0
	  },
          "reference_count": {
            "type": "integer",
            "minimum": 0
          },
          "signals": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "controls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "watch_id": {
            "type": "integer"
          },
          "batch_server": {
            "type": "integer"
          },
          "profile_name": {
            "type": "string"
          }
        },
        "required": ["client_pid", "client_uid", "client_gid", "create_time", "signals", "controls"],
        "additionalProperties": false
    }
"""
