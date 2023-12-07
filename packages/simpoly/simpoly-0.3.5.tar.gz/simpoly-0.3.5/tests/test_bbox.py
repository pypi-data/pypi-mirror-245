import random
from random import randint

import pytest
import torch
import torchvision.ops as ops

from simpoly import bbox_utils

torch.set_grad_enabled(False)
random.seed(0)


def rand_boxes(n: int):
    return [bbox_utils.random_bbox() for _ in range(n)]


def test_iou():
    # Setup
    n = randint(10, 100)
    m = randint(10, 100)
    boxes1, boxes2 = rand_boxes(n), rand_boxes(m)

    # Compute IoU
    iou = torch.tensor(bbox_utils.get_iou_matrix(boxes1, boxes2))
    iou_torch = ops.box_iou(torch.tensor(boxes1), torch.tensor(boxes2))

    assert (iou - iou_torch).abs().mean() < 1e-5, "Incorrect IoU"


def test_nms():
    # Setup
    n = randint(100, 500)
    boxes = rand_boxes(n)
    classes = [randint(0, 5) for _ in range(n)]
    scores = [(x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in boxes]
    t_boxes = torch.tensor(boxes)
    t_scores = torch.tensor(scores)
    t_classes = torch.tensor(classes)

    # NMS
    keep_torch = ops.nms(t_boxes, t_scores, 0.6).tolist()
    keep = bbox_utils.nms(boxes, scores, 0.6)
    b_keep_torch = ops.batched_nms(t_boxes, t_scores, t_classes, 0.6).tolist()
    b_keep = bbox_utils.batched_nms(boxes, scores, classes, 0.6)

    # Check
    assert set(keep) == set(keep_torch)
    assert set(b_keep) == set(b_keep_torch)
