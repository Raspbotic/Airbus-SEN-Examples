// Copyright 2026 Kapbotics
// SPDX-License-Identifier: Apache-2.0

#include "simulation_interface.h"

// The namespace MUST match your CMake target name!
namespace simulation_interface_package {

    // Bring your implementation classes into this namespace 
    // so the SEN macro can resolve them correctly.
    using sim_interface::OwnshipImpl;
    using sim_interface::RadarReportImpl;

    // Export them to the SEN Runtime
    SEN_EXPORT_CLASS(OwnshipImpl)
    SEN_EXPORT_CLASS(RadarReportImpl)

} // namespace simulation_interface_package