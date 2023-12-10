#pragma once

#include "nano_fmm/types.hpp"
#include "nano_fmm/config.hpp"
#include "nano_fmm/polyline.hpp"

#include "nano_fmm/network/projected_point.hpp"
#include "nano_fmm/network/ubodt.hpp"
#include "nano_fmm/network/match_result.hpp"

#include "packedrtree.hpp"

#include <optional>
#include <memory>
#include <vector>
#include <map>

namespace nano_fmm
{
struct Network
{
    Network(bool is_wgs84 = true) : is_wgs84_(is_wgs84) {}
    bool is_wgs84() const { return is_wgs84_; }

    // road network
    bool add_road(const Eigen::Ref<const RowVectors> &geom, int64_t road_id);
    bool add_link(int64_t source_road, int64_t target_road,
                  bool check_road = false);
    bool remove_road(int64_t road_id);
    bool remove_link(int64_t source_road, int64_t target_road);

    bool has_road(int64_t road_id) const;
    bool has_link(int64_t source_road, int64_t target_road) const;

    std::vector<int64_t> prev_roads(int64_t road_id) const;
    std::vector<int64_t> next_roads(int64_t road_id) const;
    std::vector<int64_t> roads() const;
    const Polyline *road(int64_t road_id) const;

    // config
    const Config &config() const { return config_; }
    Config &config() { return config_; }
    Network &config(const Config &new_config)
    {
        config_ = new_config;
        return *this;
    }

    // query: Candidate search (CS)
    std::vector<ProjectedPoint>
    query(const Eigen::Vector3d &position, double radius,
          std::optional<int> k = std::nullopt,
          std::optional<double> z_max_offset = std::nullopt) const;
    std::map<std::tuple<int64_t, int64_t>, RowVectors>
    query(const Eigen::Vector4d &bbox) const;

    // traj
    MatchResult match(const RowVectors &trajectory) const;

    // build cache (not necessary), 0 -> seq, 1 -> par, 2 -> par_unseq
    void build(int execution_polylicy = 2) const;
    void reset() const;

    // graph operations
    // move forward/backward N meters, return ProjectPoint
    // single source dijkstra

    // load&dump
    static std::unique_ptr<Network> load(const std::string &path);
    bool dump(const std::string &path, bool indent = true,
              bool as_geojson = true) const;
    // ubodt
    std::vector<UbodtRecord>
    build_ubodt(std::optional<double> thresh = std::nullopt) const;
    std::vector<UbodtRecord>
    build_ubodt(const std::vector<int64_t> &roads,
                std::optional<double> thresh = std::nullopt) const;
    size_t clear_ubodt();
    size_t load_ubodt(const std::vector<UbodtRecord> &rows);
    bool load_ubodt(const std::string &path);
    bool dump_ubodt(const std::string &path,
                    std::optional<double> thresh) const;

    // to 2d, z will be set to zero
    Network to_2d() const;

    Network &from_geojson(const RapidjsonValue &json);
    RapidjsonValue to_geojson(RapidjsonAllocator &allocator) const;
    RapidjsonValue to_geojson() const
    {
        RapidjsonAllocator allocator;
        return to_geojson(allocator);
    }

    Network &from_rapidjson(const RapidjsonValue &json);
    RapidjsonValue to_rapidjson(RapidjsonAllocator &allocator) const;
    RapidjsonValue to_rapidjson() const
    {
        RapidjsonAllocator allocator;
        return to_rapidjson(allocator);
    }

  private:
    bool is_wgs84_ = true;
    // roads (id -> geom)
    unordered_map<int64_t, Polyline> roads_;
    // links (id -> {nexts}, id -> {prevs})
    unordered_map<int64_t, unordered_set<int64_t>> nexts_, prevs_;
    // config
    Config config_;

    // spatial index
    mutable std::vector<IndexIJ> segs_;
    mutable unordered_map<IndexIJ, size_t, hash_eigen<IndexIJ>> seg2idx_;
    mutable std::optional<FlatGeobuf::PackedRTree> rtree_;
    FlatGeobuf::PackedRTree &rtree() const;

    using IndexMap = unordered_map<int64_t, int64_t>;
    using DistanceMap = unordered_map<int64_t, double>;
    void single_source_upperbound_dijkstra(int64_t source, double distance, //
                                           IndexMap &predecessor_map,
                                           DistanceMap &distance_map) const;
    unordered_map<IndexIJ, UbodtRecord, hash_eigen<IndexIJ>> ubodt_;
};
} // namespace nano_fmm
