#!/usr/bin/env bash
# Headed, slowed-down run of the mock flows: good for the demo recording.
set -e
cd "$(dirname "$0")/.."
pytest -m mock --headed --slowmo 400 "$@"
