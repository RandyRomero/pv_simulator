# pv_simulator
A task assignment

# pv_simulator

A simple task assignment.
An app that consumes messages from the broker, specifically messages with meter values.
It also generates corresponding pv simulator values, then sums app both values
and writes to a file on a disk - to /pv_simulator/logs/output.log file

### Requirements

Requires running rabbitmq. Host, port, login, password can be configured
via environment variables.

### Installation
`git clone git@github.com:RandyRomero/pv_simulator.git`

`cd pv_simulator`

`poetry shell`

`poetry install`

### Formatting and CI

`make format`

`make check`

### Tests

To be written