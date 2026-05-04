#!/bin/bash
set -e
cd ~/.hermes
python3 -m venv venv_oracle
source venv_oracle/bin/activate
pip install --upgrade pip setuptools wheel
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install "axolotl[flash-attn]" git+https://github.com/OpenAccess-AI-Collective/axolotl.git
python -c "import torch; print('torch', torch.__version__, 'CUDA:', torch.cuda.is_available())"
python -c "import axolotl; print('axolotl OK')"
echo "=== READY ==="
