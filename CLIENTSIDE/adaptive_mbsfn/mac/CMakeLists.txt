#
# Copyright 2013-2021 Software Radio Systems Limited
#
# This file is part of srsRAN
#
# srsRAN is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# srsRAN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# A copy of the GNU Affero General Public License can be found in
# the LICENSE file in the top-level directory of this distribution
# and at http://www.gnu.org/licenses/.
#

add_subdirectory(schedulers)

set(SOURCES mac.cc ue.cc sched.cc sched_carrier.cc sched_grid.cc sched_ue_ctrl/sched_harq.cc sched_ue.cc
        sched_ue_ctrl/sched_lch.cc sched_ue_ctrl/sched_ue_cell.cc sched_phy_ch/sf_cch_allocator.cc sched_phy_ch/sched_dci.cc sched_helpers.cc network_components/client.cc)
add_library(srsenb_mac STATIC ${SOURCES} $<TARGET_OBJECTS:mac_schedulers>)

set(SOURCES mac_nr.cc)
add_library(srsgnb_mac STATIC ${SOURCES})
