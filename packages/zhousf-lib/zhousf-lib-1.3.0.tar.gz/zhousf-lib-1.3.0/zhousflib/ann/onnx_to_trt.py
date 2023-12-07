# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/12/5 
# @Function:
import os
from pathlib import Path

import tensorrt as trt

"""
############## 安装CUDA ##############
CUDA下载：https://developer.nvidia.com/cuda-toolkit-archive
【windows】
新建系统环境变量：CUDA_PATH=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0
新建系统环境变量：CUDA_PATH_V12_0=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0
验证：在cmd中运行 nvcc -V


############## 安装cudnn ##############
cudnn下载：https://developer.nvidia.com/rdp/cudnn-archive
【windows】
将目录下的bin、lib（lib选择x64）、include文件夹复制到C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/12.0目录中
添加系统环境变量：Path=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/bin
添加系统环境变量：Path=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/libnvvp
验证：
在cmd中运行 C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/extras/demo_suite/deviceQuery.exe
显示Result = PASS则成功


############## 安装tensorRT ##############
官方文档：https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/quick-start-guide/index.html
tensorrt下载：https://developer.nvidia.com/nvidia-tensorrt-8x-download
【windows】
将目录下的bin、lib（lib选择x64）、include文件夹复制到C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/12.0目录中
添加系统环境变量：Path=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/bin
添加系统环境变量：Path=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/libnvvp
添加系统环境变量：Path=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/include
添加系统环境变量：Path=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.0/lib/x64
设置完后重启电脑
pip install TensorRT-8.6.1.6/uff/uff-0.6.9-py2.py3-none-any.whl
pip install TensorRT-8.6.1.6/graphsurgeon/graphsurgeon-0.4.6-py2.py3-none-any.whl
pip install TensorRT-8.6.1.6/onnx_graphsurgeon/onnx_graphsurgeon-0.3.12-py2.py3-none-any.whl

【linux】
tensorrt下载：https://developer.nvidia.com/nvidia-tensorrt-8x-download
解压：tar -zxvf TensorRT-8.6.1.6.Linux.x86_64-gnu.cuda-11.8.tar.gz
cd TensorRT-8.6.1.6/python
python -m pip install tensorrt-8.6.1-cp39-none-linux_x86_64.whl
配置环境变量
vim ~/.bashrc
export LD_LIBRARY_PATH=/root/zhousf/tensorrt/TensorRT-8.6.1.6/lib:$LD_LIBRARY_PATH
source ~/.bashrc

验证：
import tensorrt as trt
print(trt.__version__)


############## 安装pycuda ##############
pip install pycuda
验证：
import pycuda.autoinit
import pycuda.driver as drv
drv.init()
print("CUDA device count:", drv.Device.count())
"""


def check_shape(shape: dict):
    assert shape, "请指定shape，例如：shape={0}".format({"input_ids": [(10, 128), (10, 128), (10, 128)],
                                                  "token_type_ids": [(10, 128), (10, 128), (10, 128)],
                                                  "attention_mask": [(10, 128), (10, 128), (10, 128)]})
    for name in shape:
        assert len(shape.get(name)) == 3, "shape必须包含minShapes，optShapes，maxShapes三个，例如：shape={0}，但是输入为：{1}".format(
            {"input_ids": [(10, 128), (10, 128), (10, 128)]}, shape.get(name))


def convert_trt_by_command(onnx_file_path: Path, save_trt_path: Path, shape: dict):
    """
    采用trtexec工具将onnx转换成trt
    :param onnx_file_path: Path(r"model.onnx")
    :param save_trt_path: Path(r"model.trt")
    :param shape:  {"input_ids": [(10, 128), (10, 128), (10, 128)],
                   "token_type_ids": [(10, 128), (10, 128), (10, 128)],
                   "attention_mask": [(10, 128), (10, 128), (10, 128)]}
    :return:
    convert_trt_by_command(onnx_file_path=Path(r"model.onnx"), save_trt_path=model.trt"),
                       shape={"input_ids": [(10, 128), (10, 128), (10, 128)],
                              "token_type_ids": [(10, 128), (10, 128), (10, 128)],
                              "attention_mask": [(10, 128), (10, 128), (10, 128)]})
    """
    """
    --fp16   FP16量化精度
    --int8   INT8量化精度
    --best   FP32+FP16+INT8同时使用，找一个速度最快的
    --minShapes  动态Shape指定(--maxShapes=input0:1x3x256x256,input1:1x3x128x128)
    --optShapes  动态Shape指定(--maxShapes=input0:1x3x256x256,input1:1x3x128x128)
    --maxShapes  动态Shape指定(--maxShapes=input0:1x3x256x256,input1:1x3x128x128)
    --inputIOFormats  指定模型输入精度与数据排布格式，默认fp32:chw(--inputIOFormats=fp16:chw)
    --outputIOFormats 指定模型输输出精度与数据排布格式，默认fp32:chw(--outputIOFormats=fp16:chw)
    --memPoolSize   内存池大小(--memPoolSize =workspace:1024.5,dlaSRAM:256)
    --profilingVerbosity  打印信息的详细程度layer_names_only|detailed|none(--profilingVerbosity=detailed)
    --explicitBatch  与固化onnx的batch size一致
    --useCudaGraph 
    """
    check_shape(shape)
    min_shapes = [shape.get(name)[0] for name in shape]
    opt_shapes = [shape.get(name)[1] for name in shape]
    max_shapes = [shape.get(name)[2] for name in shape]
    names = list(shape.keys())
    min_shapes_str = ""
    opt_shapes_str = ""
    max_shapes_str = ""
    for i in range(0, len(names)):
        min_shapes_str += "{0}:{1},".format(names[i], "x".join([str(item) for item in min_shapes[i]]))
        opt_shapes_str += "{0}:{1},".format(names[i], "x".join([str(item) for item in opt_shapes[i]]))
        max_shapes_str += "{0}:{1},".format(names[i], "x".join([str(item) for item in max_shapes[i]]))
    command = "trtexec " \
              "--onnx={0} " \
              "--saveEngine={1} " \
              "--minShapes={2} " \
              "--optShapes={3} " \
              "--maxShapes={4} ".format(onnx_file_path, save_trt_path, min_shapes_str, opt_shapes_str, max_shapes_str)
    os.system(command)
    print("done.")


def convert_trt(onnx_file_path: Path, save_trt_path: Path, shape: dict, max_batch_size: int = 8):
    """
    采用OnnxParser将onnx转换成trt【推荐使用】
    :param onnx_file_path:
    :param save_trt_path:
    :param shape:  {"input_ids": [(10, 128), (10, 128), (10, 128)],
                   "token_type_ids": [(10, 128), (10, 128), (10, 128)],
                   "attention_mask": [(10, 128), (10, 128), (10, 128)]}
    :param max_batch_size:
    :return:
    """

    def GiB(val):
        return val * 1 << 30

    check_shape(shape)
    assert max_batch_size <= 8, "trt推理时最大支持的batch_size=8，但是输入为：{0}".format(max_batch_size)
    G_LOGGER = trt.Logger(trt.Logger.WARNING)
    explicit_batch = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    with trt.Builder(G_LOGGER) as builder, builder.create_network(explicit_batch) as network, \
            trt.OnnxParser(network, G_LOGGER) as parser:
        builder.max_batch_size = max_batch_size
        config = builder.create_builder_config()
        config.max_workspace_size = GiB(2)
        config.set_flag(trt.BuilderFlag.FP16)
        print('Loading ONNX file from path {}...'.format(onnx_file_path))
        with open(onnx_file_path, 'rb') as model:
            print('Beginning ONNX file parsing')
            parser.parse(model.read())
        print('Completed parsing of ONNX file')
        print('Building an engine from file {}; this may take a while...'.format(onnx_file_path))
        profile = builder.create_optimization_profile()
        for name in shape:
            profile.set_shape(name, *shape.get(name))
        config.add_optimization_profile(profile)
        engine = builder.build_engine(network, config)
        assert engine
        print("Completed creating Engine")
        with open(save_trt_path, "wb") as f:
            f.write(engine.serialize())
        print("done.")


if __name__ == "__main__":
    # convert_trt_by_command(onnx_file_path=Path(r"F:\torch\onnx\model.onnx"),
    #                        save_trt_path=Path(r"F:\torch\onnx\model.trt"),
    #                        shape={"input_ids": [(10, 128), (10, 128), (10, 128)],
    #                               "token_type_ids": [(10, 128), (10, 128), (10, 128)],
    #                               "attention_mask": [(10, 128), (10, 128), (10, 128)]})
    convert_trt(onnx_file_path=Path(r"F:\torch\onnx\model.onnx"),
                save_trt_path=Path(r"F:\torch\onnx\model.trt"),
                shape={"input_ids": [(10, 128), (10, 128), (10, 128)],
                       "token_type_ids": [(10, 128), (10, 128), (10, 128)],
                       "attention_mask": [(10, 128), (10, 128), (10, 128)]})
    pass

