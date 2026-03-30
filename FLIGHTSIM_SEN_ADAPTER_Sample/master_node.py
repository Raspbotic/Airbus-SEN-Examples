# master_node.py
# Copyright 2026 Kapbotics
# SPDX-License-Identifier: Apache-2.0

import pcs_node
import se_node
import monitor_node

def run():
    # Initialize all nodes sequentially
    pcs_node.run()
    se_node.run()
    monitor_node.run()

def update():
    # Update all nodes synchronously within the single SEN Kernel loop
    pcs_node.update()
    se_node.update()
    monitor_node.update()

def stop():
    # Clean up sockets
    pcs_node.stop()
    se_node.stop()