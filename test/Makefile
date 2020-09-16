TVM_DIR = $(abspath ..)/3rdparty/incubator-tvm
VTA_DIR = $(TVM_DIR)/3rdparty/vta-hw
DMLC_DIR = $(TVM_DIR)/3rdparty/dmlc-core
DLPACK_DIR = $(TVM_DIR)/3rdparty/dlpack

VTA_DEFS = $(shell python3 $(VTA_DIR)/config/vta_config.py --use-cfg=$(VTA_DIR)/config/vta_config.json --defs)

VTA_FILES = \
sim_driver.cc \
$(VTA_DIR)/src/sim/sim_tlpp.cc \
$(VTA_DIR)/src/vmem/virtual_memory.cc

default: test
	./test

test: test.cc
	g++ \
	-std=c++14 \
	$(VTA_DEFS) \
	$(VTA_FILES) \
	$< \
	-o $@ \
	-I$(VTA_DIR)/include \
	-I$(VTA_DIR)/src/vmem \
	-I$(TVM_DIR)/include \
	-I$(DMLC_DIR)/include \
	-I$(DLPACK_DIR)/include

lib.so:
	g++ \
	-std=c++14 \
	-fpic \
	-shared \
	-o $@ \
	$(VTA_DEFS) \
	$(VTA_FILES) \
	-I$(VTA_DIR)/include \
	-I$(VTA_DIR)/src/vmem \
	-I$(TVM_DIR)/include \
	-I$(DMLC_DIR)/include \
	-I$(DLPACK_DIR)/include
