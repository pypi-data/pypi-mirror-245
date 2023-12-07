# Copyright 2021 The TensorFlow GNN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Unit tests for generate training data test."""

from os import path

from absl import flags
import tensorflow as tf
from tensorflow_gnn.tools import generate_training_data
from tensorflow_gnn.utils import test_utils


FLAGS = flags.FLAGS


class GenerateDataTest(tf.test.TestCase):

  def test_generate_training_data(self):
    schema_filename = test_utils.get_resource("examples/schemas/mpnn.pbtxt")
    output_filename = path.join(FLAGS.test_tmpdir, "examples.tfrecords")
    generate_training_data.generate_training_data(
        schema_filename, output_filename, "tfrecord", 64)
    self.assertTrue(path.exists(output_filename))


if __name__ == "__main__":
  tf.test.main()
