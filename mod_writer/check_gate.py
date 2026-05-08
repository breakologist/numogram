#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer')
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer-composer/scripts')

from composer_extension import ZoneComposer, patch_mod_composer
from mod_writer.composer import ModComposer
patch_mod_composer()

c = ModComposer()
zc = ZoneComposer(c)
print("Gate for aq=4:", zc._gate_from_aq('4'))
print("Gate for aq=6:", zc._gate_from_aq('6'))
