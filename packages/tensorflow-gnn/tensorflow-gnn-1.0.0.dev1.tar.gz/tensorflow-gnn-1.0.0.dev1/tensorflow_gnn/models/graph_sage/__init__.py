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
"""GraphSAGE.

Users of TF-GNN can use this model by importing it next to the core library as

```python
import tensorflow_gnn as tfgnn
from tensorflow_gnn.models import graph_sage
```
"""

from tensorflow_gnn.models.graph_sage import layers
from tensorflow_gnn.utils import api_utils

# NOTE: This package is covered by tensorflow_gnn/api_def/api_symbols_test.py.
# Please see there for instructions how to reflect API changes.
# LINT.IfChange

GCNGraphSAGENodeSetUpdate = layers.GCNGraphSAGENodeSetUpdate
GraphSAGEAggregatorConv = layers.GraphSAGEAggregatorConv
GraphSAGEPoolingConv = layers.GraphSAGEPoolingConv
GraphSAGENextState = layers.GraphSAGENextState
GraphSAGEGraphUpdate = layers.GraphSAGEGraphUpdate

# Remove all names added by module imports, unless explicitly allowed here.
api_utils.remove_submodules_except(__name__, [])
# LINT.ThenChange(../../api_def/graph_sage-symbols.txt)
