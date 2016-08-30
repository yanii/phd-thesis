#!/bin/bash

for file in chainer-mnist-ablate*/hist.log; do grep ablate_test_acc_diff_ $file | sed 's/ablate_test_acc_diff_\([0-9]\+\)\.npy/\1/'|sort -n > "`dirname $file`-hist-test-acc.log"; done
for file in chainer-mnist-ablate*/hist.log; do grep ablate_train_acc_diff_ $file | sed 's/ablate_train_acc_diff_\([0-9]\+\)\.npy/\1/'|sort -n > "`dirname $file`-hist-train-acc.log"; done
for file in chainer-mnist-ablate*/hist.log; do grep ablate_test_loss_diff_ $file | sed 's/ablate_test_loss_diff_\([0-9]\+\)\.npy/\1/'|sort -n > "`dirname $file`-hist-test-loss.log"; done
for file in chainer-mnist-ablate*/hist.log; do grep ablate_train_loss_diff_ $file | sed 's/ablate_train_loss_diff_\([0-9]\+\)\.npy/\1/'|sort -n > "`dirname $file`-hist-train-loss.log"; done

