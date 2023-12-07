/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
// This file is auto-generated. See "generate_kernels.py"
#ifndef XFORMERS_MEM_EFF_ATTENTION_DISABLE_BACKWARD
#include "../../kernel_backward.h"
__global__ void __launch_bounds__(
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::kNumThreads,
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::kMinBlocksPerSm)
fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80(typename AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::Params p) {
#ifdef __CUDA_ARCH__
#if __CUDA_ARCH__ >= 800
#if __CUDA_ARCH__ < 1000
  if (!p.advance_to_block()) {
    return;
  }
  AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128, true>::attention_kernel(p);
  return;
#endif
#endif
    printf(
        "FATAL: kernel `fmha_cutlassB_bf16_aligned_128x128_k128_seqaligned_sm80` is for sm80-sm100, but was built for sm%d\n",
        int(__CUDA_ARCH__ + 0) / 10);
#endif
}
__global__ void __launch_bounds__(
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128>::kNumThreads,
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128>::kMinBlocksPerSm)
fmha_cutlassB_bf16_aligned_128x128_k128_sm80(typename AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128>::Params p) {
#ifdef __CUDA_ARCH__
#if __CUDA_ARCH__ >= 800
#if __CUDA_ARCH__ < 1000
  if (!p.advance_to_block()) {
    return;
  }
  AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, true, 128, 128, 128>::attention_kernel(p);
  return;
#endif
#endif
    printf(
        "FATAL: kernel `fmha_cutlassB_bf16_aligned_128x128_k128_sm80` is for sm80-sm100, but was built for sm%d\n",
        int(__CUDA_ARCH__ + 0) / 10);
#endif
}
__global__ void __launch_bounds__(
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128, true>::kNumThreads,
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128, true>::kMinBlocksPerSm)
fmha_cutlassB_bf16_aligned_64x64_k128_seqaligned_sm80(typename AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128, true>::Params p) {
#ifdef __CUDA_ARCH__
#if __CUDA_ARCH__ >= 800
#if __CUDA_ARCH__ < 1000
  if (!p.advance_to_block()) {
    return;
  }
  AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128, true>::attention_kernel(p);
  return;
#endif
#endif
    printf(
        "FATAL: kernel `fmha_cutlassB_bf16_aligned_64x64_k128_seqaligned_sm80` is for sm80-sm100, but was built for sm%d\n",
        int(__CUDA_ARCH__ + 0) / 10);
#endif
}
__global__ void __launch_bounds__(
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128>::kNumThreads,
    AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128>::kMinBlocksPerSm)
fmha_cutlassB_bf16_aligned_64x64_k128_sm80(typename AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128>::Params p) {
#ifdef __CUDA_ARCH__
#if __CUDA_ARCH__ >= 800
#if __CUDA_ARCH__ < 1000
  if (!p.advance_to_block()) {
    return;
  }
  AttentionBackwardKernel<cutlass::arch::Sm80, cutlass::bfloat16_t, true, false, false, 64, 64, 128>::attention_kernel(p);
  return;
#endif
#endif
    printf(
        "FATAL: kernel `fmha_cutlassB_bf16_aligned_64x64_k128_sm80` is for sm80-sm100, but was built for sm%d\n",
        int(__CUDA_ARCH__ + 0) / 10);
#endif
}
#endif // XFORMERS_MEM_EFF_ATTENTION_DISABLE_BACKWARD
