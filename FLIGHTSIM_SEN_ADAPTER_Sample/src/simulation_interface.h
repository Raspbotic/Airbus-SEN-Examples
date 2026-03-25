#pragma once
#include <string>
#include "stl/sim_interface/simulation_interface.stl.h"
#include "sen/kernel/component_api.h"

namespace sim_interface {

    class OwnshipImpl : public OwnshipBase {
    public:
        SEN_NOCOPY_NOMOVE(OwnshipImpl)

            OwnshipImpl(const std::string& name, const sen::VarMap& args) : OwnshipBase(name, args) {}
        ~OwnshipImpl() override = default;

        void update(sen::kernel::RunApi& runApi) override {
            std::ignore = runApi;
        }

    protected:
        // Matches line 133 of the generated file exactly
        void updateStateImpl(const std::string& id, f64 la, f64 lo, f64 al, f64 h, f64 p, f64 r) override {
            this->setNextOwnshipId(id);
            this->setNextLat(la);
            this->setNextLon(lo);
            this->setNextAltM(al);
            this->setNextHdg(h);
            this->setNextPitch(p);
            this->setNextRoll(r);
        }
    };

    class RadarReportImpl : public RadarReportBase {
    public:
        SEN_NOCOPY_NOMOVE(RadarReportImpl)

            RadarReportImpl(const std::string& name, const sen::VarMap& args) : RadarReportBase(name, args) {}
        ~RadarReportImpl() override = default;

        void update(sen::kernel::RunApi& runApi) override {
            std::ignore = runApi;
        }

    protected:
        // Matches line 462 of the generated file exactly
        void setDetectionImpl(const std::string& id, f64 rng, bool det) override {
            this->setNextEmitterId(id);
            this->setNextRangeM(rng);
            this->setNextIsDetected(det);
        }
    };

} // namespace sim_interface