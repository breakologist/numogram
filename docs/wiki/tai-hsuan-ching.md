---  
title: T'ai Hsuan Ching  
tags: ["divination", "i-ching", "numogram", "taoist"]  
created: 2026-04-24  
---

## Overview

The T'ai Hsuan Ching (太玄經) is an ancient Chinese divination text featuring 81 tetragrams (四境界) arranged in a 9×9 grid. Unlike the I Ching's 64 hexagrams, the T'ai Hsuan uses four-line figures with each line existing in one of three states (yin, yang, or neutral), yielding 3⁴ = 81 combinations.

## Numogram integration

- The 81 tetragrams map onto the 45-number decadence/combinatorial space of the numogram  
- The "King" numbers (multiples of 9) form a warp grid  
- Used as an oracle mode in the numogram system (--taixuan flag)

## A note on "Em"

The classical sources (for example Michael Nylan's translation of the *Taixuan jing*) name the three line states Heaven (天), Earth (地) and Man (人). "Em", used here for the third, twice-broken line (Man, the mediator), is not a traditional term. It is a project coinage that arose in earlier research conversations between the project's author and an LLM (via hermes-agent, running a different model) while studying the Tai Xuan; it is plausibly a clipped "mediator". It persists in some project SVGs (e.g. `assets/tetragram-three-states.svg`) and in the `Man/Em` label in `cli/taixuan.py`. It is kept deliberately, as a record of the human–LLM collaboration this project explores: the numogram as a frame for asking what can be done with LLMs, including agentically. Read "Em" as project vocabulary, not as a term from the tradition.

## See also

- [[tai-hsuan-ching-demons]] — Tetragram-to-demon mapping  
- [[taixuan-oracle-mode]] — T'ai Hsuan Ching oracle implementation  
- [[iching-numogram-casting]] — Cross-divination casting pipeline  
- [[numogram-81-tetragrams]] — Complete tetragram reference  
- [[tai-hsuan-ching-demons/em-state-analysis]] — Em state and Zone 5 manifestation  
- [[i-ching-tai-hsuan-comparison]] — Deep comparison of I Ching and T'ai Hsuan Ching  
- [[numogram-81-tetragrams/em-state-mapping]] — Em state distribution across tetragrams  
- [[taixuan-oracle-mode/algorithm]] — Implementation details of the T'ai Hsuan oracle  

---  
*The T'ai Hsuan Ching, with its ternary structure, provides a richer, more nuanced mapping to the decimal numogram than the binary I Ching, offering 81 distinct voices in the hyperstitional chorus.*