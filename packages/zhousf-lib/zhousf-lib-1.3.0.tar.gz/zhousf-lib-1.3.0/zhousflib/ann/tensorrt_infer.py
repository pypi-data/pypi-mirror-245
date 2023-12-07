# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/12/7 
# @Function: 参考 https://github.com/NVIDIA/TensorRT/blob/master/samples/python/common.py
import os
os.environ["CUDA_MODULE_LOADING"] = "LAZY"
import copy
from pathlib import Path

import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
import tensorrt as trt

try:
    # Sometimes python does not understand FileNotFoundError
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


# Simple helper data class that's a little nicer to use than a 2-tuple.
class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    def __repr__(self):
        return self.__str__()


# This function is generalized for multiple inputs/outputs.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference(context, bindings, inputs, outputs, stream, batch_size=1):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    # Run inference.
    context.execute_async(batch_size=batch_size, bindings=bindings, stream_handle=stream.handle)
    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Synchronize the stream
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]


# This function is generalized for multiple inputs/outputs for full dimension networks.
# inputs and outputs are expected to be lists of HostDeviceMem objects.
def do_inference_v2(context, bindings, inputs, outputs, stream):
    # Transfer input data to the GPU.
    [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
    # Run inference.
    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
    # Transfer predictions back from the GPU.
    [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
    # Synchronize the stream
    stream.synchronize()
    # Return only the host outputs.
    return [out.host for out in outputs]


class RTInfer(object):

    def __init__(self, trt_file_path: Path):
        with trt_file_path.open("rb") as f:
            runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
            self.engine = runtime.deserialize_cuda_engine(f.read())
            self.context = self.engine.create_execution_context()
            self.stream = cuda.Stream()

    def infer(self, input: np.asarray):
        inputs = []
        outputs = []
        bindings = []
        for binding in self.engine:
            size = trt.volume(self.engine.get_binding_shape(binding)) * self.engine.max_batch_size
            dtype = trt.nptype(self.engine.get_binding_dtype(binding))
            # Allocate host and device buffers
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)
            # Append the device buffer to device bindings.
            bindings.append(int(device_mem))
            # Append to the appropriate list.
            if self.engine.binding_is_input(binding):
                if batch is not None:
                    input_memory = cuda.mem_alloc(batch.nbytes)
                    # 转换为内存连续存储的数组，提高运行效率
                    input_buffer = np.ascontiguousarray(batch)
                    inputs.append(HostDeviceMem(input_buffer, input_memory))
                else:
                    inputs.append(HostDeviceMem(host_mem, device_mem))
            else:
                outputs.append(HostDeviceMem(host_mem, device_mem))
        return do_inference_v2(context=self.context, bindings=bindings, inputs=inputs, outputs=outputs, stream=self.stream)


if __name__ == "__main__":
    from zhousflib.ann.torch_to_onnx import to_numpy, example_inputs_demo
    args = example_inputs_demo()
    batch = [to_numpy(args[0]), to_numpy(args[1]), to_numpy(args[2])]
    batch = np.asarray(batch)
    rt_engine = RTInfer(trt_file_path=Path(r"F:\torch\onnx\model.trt"))
    data = rt_engine.infer(input=batch)
    data = copy.deepcopy(data)
    print(data)
