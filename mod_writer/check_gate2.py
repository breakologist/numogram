#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer')
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer-composer/scripts')

from composer_extension import ZoneComposer, patch_mod_composer
from mod_writer.composer import ModComposer
patch_mod_composer()

c = ModComposer()
zc = ZoneComposer(c)
print("zc has .composer?", hasattr(zc, 'composer'))
print("zc.composer is c?", getattr(zc, 'composer', None) is c)
print("zc has _zone_composer?", hasattr(zc, '_zone_composer'))
# Check what the batch generator actually does (line 55):
# gate = zc.composer._zone_composer._gate_from_aq(str(aq)) if hasattr(zc.composer, '_zone_composer') else None
# But zc.composer likely returns the inner ModComposer, which probably doesn't have _zone_composer
# Actually ZoneComposer wraps and exposes methods directly; it likely has the gate method itself
print("\nDirect gate call on zc:", zc._gate_from_aq('4'))
