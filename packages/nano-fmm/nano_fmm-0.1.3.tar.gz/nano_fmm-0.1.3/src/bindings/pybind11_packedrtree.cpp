#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "packedrtree.hpp"

#include "spdlog/spdlog.h"
// fix exposed macro 'GetObject' from wingdi.h (included by spdlog.h) under
// windows, see https://github.com/Tencent/rapidjson/issues/1448
#ifdef GetObject
#undef GetObject
#endif

#include "nano_fmm/types.hpp"

namespace nano_fmm
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

void bind_packedrtree(py::module &m)
{
    using namespace FlatGeobuf;
    py::class_<NodeItem>(m, "NodeItem", py::module_local()) //
        .def(py::init<>())
        .def(py::init<double, double, double, double, uint64_t>(), //
             "minX"_a, "minY"_a,                                   //
             "maxX"_a, "maxY"_a,                                   //
             "offset"_a = 0)
        .def(py::init([](const Eigen::Vector2d &min, //
                         const Eigen::Vector2d &max, //
                         uint64_t offset) {
                 return new NodeItem{min[0], min[1], max[0], max[1], offset};
             }),
             "min"_a, "max"_a, "offset"_a = 0)
        .def(
            py::init([](const Eigen::Vector4d &bbox, uint64_t offset) {
                return new NodeItem{bbox[0], bbox[1], bbox[2], bbox[3], offset};
            }),
            "bbox"_a, "offset"_a = 0)
        .def_readwrite("minX", &NodeItem::minX)
        .def_readwrite("minY", &NodeItem::minY)
        .def_readwrite("maxX", &NodeItem::maxX)
        .def_readwrite("maxY", &NodeItem::maxY)
        .def_readwrite("offset", &NodeItem::offset)
        .def("width", &NodeItem::width)
        .def("height", &NodeItem::height)
        .def_static("sum", &NodeItem::sum, "a"_a, "b"_a)
        .def_static("create", &NodeItem::create, "offset"_a = 0)
        .def("expand", &NodeItem::expand, "r"_a)
        .def("intersects", &NodeItem::intersects, "r"_a)
        .def(
            "intersects",
            [](const NodeItem &self, double minX, double minY, double maxX,
               double maxY) {
                return self.intersects({minX, minY, maxX, maxY});
            },
            "minX"_a, "minY"_a, "maxX"_a, "maxY"_a)
        .def("to_numpy",
             [](const NodeItem &self) {
                 return Eigen::Vector4d(self.minX, self.minY, //
                                        self.maxX, self.maxY);
             })
        .def("__repr__",
             [](const NodeItem &n) {
                 return fmt::format(
                     "NodeItem(min=[{},{}],max=[{},{}],offset={})", n.minX,
                     n.minY, n.maxX, n.maxY, n.offset);
             })
        //
        .def(py::self == py::self)
        //
        .def_static("_size_", []() { return sizeof(NodeItem); });
    py::class_<Item>(m, "Item", py::module_local()) //
        .def(py::init<>())
        .def_readwrite("nodeItem", &Item::nodeItem)
        //
        ;
    py::class_<SearchResultItem>(m, "SearchResultItem", py::module_local()) //
        .def(py::init<>())
        .def_readwrite("offset", &SearchResultItem::offset)
        .def_readwrite("index", &SearchResultItem::index)
        .def("__repr__",
             [](const SearchResultItem &self) {
                 return fmt::format("SearchResultItem(offset={},index={})",
                                    self.offset, self.index);
             })
        //
        .def(py::self == py::self)
        //
        ;

    m                                                                    //
        .def("hilbert", py::overload_cast<uint32_t, uint32_t>(&hilbert), //
             "x"_a, "y"_a)
        //
        .def(
            "hilbertSort",
            [](const std::vector<NodeItem> &items) {
                auto sorted = items;
                hilbertSort(sorted);
                return sorted;
            },
            "items"_a)
        .def(
            "calcExtent",
            [](const std::vector<NodeItem> &rects) {
                return calcExtent(rects);
            },
            "rects"_a)
        //
        ;

    py::class_<PackedRTree>(m, "PackedRTree", py::module_local()) //
        .def(py::init<const std::vector<NodeItem> &, const NodeItem &,
                      const uint16_t>(),
             "nodes"_a, "extent"_a, "nodeSize"_a = 16)
        .def(py::init([](py::buffer buf, const uint64_t numItems,
                         const uint16_t nodeSize) {
                 py::buffer_info info = buf.request();
                 return new PackedRTree(info.ptr, numItems, nodeSize);
             }),
             "data"_a, "numItems"_a, "nodeSize"_a = 16)
        .def(py::init([](const Eigen::Ref<const RowVectorsNx2> &bbox_min,
                         const Eigen::Ref<const RowVectorsNx2> &bbox_max,
                         const uint16_t node_size) {
                 auto extent = NodeItem::create();
                 const uint64_t N = bbox_min.rows();
                 auto nodes = std::vector<NodeItem>(N);
                 for (uint64_t i = 0; i < N; ++i) {
                     nodes[i].minX = bbox_min(i, 0);
                     nodes[i].minY = bbox_min(i, 1);
                     nodes[i].maxX = bbox_max(i, 0);
                     nodes[i].maxY = bbox_max(i, 1);
                     nodes[i].offset = i;
                     extent.expand(nodes[i]);
                 }
                 hilbertSort(nodes, extent);
                 return new PackedRTree(nodes, extent, node_size);
             }),
             "min"_a, "max"_a, "nodeSize"_a = 16)
        .def("search", &PackedRTree::search, //
             "minX"_a, "minY"_a,             //
             "maxX"_a, "maxY"_a)
        .def(
            "searchIndex",
            [](const PackedRTree &self,  //
               double minX, double minY, //
               double maxX, double maxY, //
               bool use_offset) {
                auto hits = self.search(minX, minY, maxX, maxY);
                const size_t N = hits.size();
                VectorUi64 idx(N);
                if (use_offset) {
                    for (size_t i = 0; i < N; ++i) {
                        idx[i] = hits[i].offset;
                    }
                } else {
                    for (size_t i = 0; i < N; ++i) {
                        idx[i] = hits[i].index;
                    }
                }
                return idx;
            },
            "minX"_a, "minY"_a, //
            "maxX"_a, "maxY"_a, py::kw_only(), "use_offset"_a = true)
        .def_static("generateLevelBounds", &PackedRTree::generateLevelBounds,
                    "numItems"_a, "nodeSize"_a)
        .def("size", py::overload_cast<>(&PackedRTree::size, py::const_))
        .def("getExtent", &PackedRTree::getExtent)
        .def("getNumItems", &PackedRTree::getNumItems)
        .def("getNumNodes", &PackedRTree::getNumNodes)
        .def("getNodeSize", &PackedRTree::getNodeSize)
        .def("to_bytes",
             [](PackedRTree &self) {
                 std::vector<uint8_t> bytes;
                 self.streamWrite([&bytes](const uint8_t *buf, size_t size) {
                     std::copy(buf, buf + size, std::back_inserter(bytes));
                 });
                 return py::bytes((const char *)bytes.data(), bytes.size());
             })

        //
        ;
}
} // namespace nano_fmm
